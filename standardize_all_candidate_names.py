import json

def fix_candidate_name(name):
    """
    Fix candidate name formatting to proper title case.
    Handles special cases like Mc/Mac prefixes, hyphens, apostrophes, and quotes.
    """
    if not name or name == "N/A":
        return name
    
    # Split on spaces
    words = name.split()
    fixed_words = []
    
    for word in words:
        # Handle words with hyphens (e.g., Stacey-Abrams)
        if '-' in word:
            parts = word.split('-')
            fixed_parts = []
            for part in parts:
                if part.startswith('Mc') and len(part) > 2:
                    # McIntosh -> McIntosh
                    fixed_parts.append('Mc' + part[2:].capitalize())
                elif part.startswith('Mac') and len(part) > 3:
                    # MacDonald -> MacDonald
                    fixed_parts.append('Mac' + part[3:].capitalize())
                else:
                    fixed_parts.append(part.capitalize())
            fixed_words.append('-'.join(fixed_parts))
        # Handle words with apostrophes (e.g., O'Brien)
        elif "'" in word:
            parts = word.split("'")
            fixed_parts = [parts[0].capitalize()]
            fixed_parts.extend([p.capitalize() for p in parts[1:]])
            fixed_words.append("'".join(fixed_parts))
        # Handle Mc/Mac prefixes
        elif word.startswith('Mc') and len(word) > 2:
            fixed_words.append('Mc' + word[2:].capitalize())
        elif word.startswith('Mac') and len(word) > 3:
            fixed_words.append('Mac' + word[3:].capitalize())
        else:
            fixed_words.append(word.capitalize())
    
    return ' '.join(fixed_words)

def standardize_candidate_names(data):
    """
    Standardize all candidate names in the results data to proper title case.
    """
    count = 0
    
    for year, year_data in data['results_by_year'].items():
        print(f"Processing year {year}...")
        
        for contest_key, contest_data in year_data.items():
            if 'results' not in contest_data:
                continue
            
            for county, county_data in contest_data['results'].items():
                # Fix dem_candidate
                if 'dem_candidate' in county_data and county_data['dem_candidate']:
                    original = county_data['dem_candidate']
                    fixed = fix_candidate_name(original)
                    if original != fixed:
                        county_data['dem_candidate'] = fixed
                        count += 1
                
                # Fix rep_candidate
                if 'rep_candidate' in county_data and county_data['rep_candidate']:
                    original = county_data['rep_candidate']
                    fixed = fix_candidate_name(original)
                    if original != fixed:
                        county_data['rep_candidate'] = fixed
                        count += 1
                
                # Fix winner_name
                if 'winner_name' in county_data and county_data['winner_name']:
                    original = county_data['winner_name']
                    fixed = fix_candidate_name(original)
                    if original != fixed:
                        county_data['winner_name'] = fixed
                        count += 1
    
    return count

def main():
    input_file = 'data/results_by_year_grouped.final.json'
    
    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Standardizing candidate names...")
    changes = standardize_candidate_names(data)
    
    print(f"\nMade {changes} changes to candidate names")
    
    print(f"Saving updated data to {input_file}...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print("✓ Done!")

if __name__ == '__main__':
    main()

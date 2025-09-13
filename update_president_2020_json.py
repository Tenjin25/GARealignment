import csv
import json
from collections import defaultdict

# For Wikipedia scraping
import requests
from bs4 import BeautifulSoup

# Input files
CSV_FILE = 'data/20201103__ga__general.csv'
JSON_FILE = 'data/ga_county_results_trimmed.json'

# Output file (backup original just in case)
OUTPUT_JSON = 'data/ga_county_results_trimmed.updated.json'

# Candidates and party mapping for president
PRESIDENT_PARTY_MAP = {
    'Joseph R. Biden': 'DEM',
    'Donald J. Trump': 'REP',
    'Jo Jorgensen': 'LIBERTARIAN',
    'Jo Jorgensen (Libertarian)': 'LIBERTARIAN',
    'Jo Jorgensen (Lib)': 'LIBERTARIAN',
    'Jo Jorgensen (Lib.)': 'LIBERTARIAN',
}

# 1. Aggregate presidential votes by county and party
county_votes = defaultdict(lambda: defaultdict(int))
with open(CSV_FILE, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # Patch: Strip whitespace from fieldnames
    reader.fieldnames = [fn.strip() for fn in reader.fieldnames]
    for row in reader:
        # Also strip whitespace from keys in each row
        row = {k.strip(): v for k, v in row.items()}
        if row['office'].strip().lower() == 'president':
            county = row['county'].strip().upper()
            candidate = row['candidate'].strip()
            party = row['party'].strip().upper()
            # Standardize party
            if candidate in PRESIDENT_PARTY_MAP:
                party = PRESIDENT_PARTY_MAP[candidate]
            # Sum all vote columns
            total_votes = sum(int(row[col] or 0) for col in [
                'election_day_votes', 'advanced_votes', 'absentee_by_mail_votes', 'provisional_votes'])
            county_votes[county][party] += total_votes

# 2. Load JSON
with open(JSON_FILE, encoding='utf-8') as f:
    data = json.load(f)


# Competitiveness scale from your JSON
COMPETITIVENESS_SCALE = {
    'Republican': [
        {"category": "Annihilation", "range": 40, "color": "#67000d"},
        {"category": "Dominant", "range": 30, "color": "#a50f15"},
        {"category": "Stronghold", "range": 20, "color": "#cb181d"},
        {"category": "Safe", "range": 10, "color": "#ef3b2c"},
        {"category": "Likely", "range": 5.5, "color": "#fb6a4a"},
        {"category": "Lean", "range": 1, "color": "#fcae91"},
        {"category": "Tilt", "range": 0.5, "color": "#fee8c8"},
    ],
    'Tossup': [
        {"category": "Tossup", "range": 0.5, "color": "#f7f7f7"}
    ],
    'Democratic': [
        {"category": "Tilt", "range": 0.5, "color": "#e1f5fe"},
        {"category": "Lean", "range": 1, "color": "#c6dbef"},
        {"category": "Likely", "range": 5.5, "color": "#9ecae1"},
        {"category": "Safe", "range": 10, "color": "#6baed6"},
        {"category": "Stronghold", "range": 20, "color": "#3182bd"},
        {"category": "Dominant", "range": 30, "color": "#08519c"},
        {"category": "Annihilation", "range": 40, "color": "#08306b"},
    ]
}

def assign_category_and_color(margin, margin_pct, winner):
    # margin: dem - rep
    # margin_pct: always positive
    if abs(margin_pct) <= 0.5:
        return 'Tossup', '#f7f7f7'
    if winner == 'REP':
        for level in COMPETITIVENESS_SCALE['Republican']:
            if margin_pct >= level['range']:
                return level['category'], level['color']
        if margin_pct >= 1:
            return "Lean", "#fcae91"
        return "Tilt", "#fee8c8"
    else:
        for level in reversed(COMPETITIVENESS_SCALE['Democratic']):
            if margin_pct >= level['range']:
                return level['category'], level['color']
        if margin_pct >= 1:
            return "Lean", "#c6dbef"
        return "Tilt", "#e1f5fe"

# --- Wikipedia scraping and cross-reference ---
def fetch_wikipedia_results():
    """Scrape Wikipedia for 2020 GA presidential results by county."""
    url = "https://en.wikipedia.org/wiki/2020_United_States_presidential_election_in_Georgia"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    table = None
    # Print all wikitable headers for debugging
    print("Searching for correct Wikipedia table...")
    for idx, t in enumerate(soup.find_all("table", class_="wikitable")):
        headers = [th.get_text(strip=True) for th in t.find_all("th")]
        print(f"Table {idx} headers: {headers[:8]}")
        # Look for table with expected headers
        if any("County" in h for h in headers) and any("Biden" in h for h in headers) and any("Trump" in h for h in headers):
            table = t
            print(f"Selected table {idx} as county results table.")
            break
    if not table:
        raise Exception("Could not find county results table on Wikipedia. See printed headers above.")
    wiki_data = {}
    header_cells = [th.get_text(" ", strip=True) for th in table.find_all("tr")[0].find_all("th")]
    # Find column indices for County, Biden, Trump, Other
    def find_col(header_options):
        for idx, h in enumerate(header_cells):
            for opt in header_options:
                if opt.lower() in h.lower():
                    return idx
        return None
    county_idx = find_col(["County"])
    biden_idx = find_col(["Joe Biden", "Biden"])
    trump_idx = find_col(["Donald Trump", "Trump"])
    other_idx = find_col(["Various candidates", "Other parties"])
    if None in (county_idx, biden_idx, trump_idx):
        print("Header cells:", header_cells)
        raise Exception("Could not find expected columns in Wikipedia table.")
    for row in table.find_all("tr")[1:]:
        cells = row.find_all(["td", "th"])
        if len(cells) < max(county_idx, biden_idx, trump_idx) + 1:
            continue
        county = cells[county_idx].get_text(strip=True).replace(" County", "").upper()
        try:
            biden_votes = int(cells[biden_idx].get_text(strip=True).replace(",", ""))
            trump_votes = int(cells[trump_idx].get_text(strip=True).replace(",", ""))
            other_votes = int(cells[other_idx].get_text(strip=True).replace(",", "")) if other_idx is not None else 0
        except Exception:
            continue
        total_votes = biden_votes + trump_votes + other_votes
        winner = 'DEM' if biden_votes > trump_votes else 'REP'
        margin = biden_votes - trump_votes
        margin_pct = (abs(margin) / (biden_votes + trump_votes) * 100) if (biden_votes + trump_votes) else 0
        wiki_data[county] = {
            'dem_votes': biden_votes,
            'rep_votes': trump_votes,
            'other_votes': other_votes,
            'winner': winner,
            'margin': margin,
            'margin_pct': round(margin_pct, 2),
            'total_votes': total_votes
        }
    return wiki_data


# 3. Update JSON for each county (CSV), then cross-check with Wikipedia
for county, votes in county_votes.items():
    dem = votes.get('DEM', 0)
    rep = votes.get('REP', 0)
    lib = votes.get('LIBERTARIAN', 0)
    total = dem + rep + lib
    margin = dem - rep
    two_party_total = dem + rep
    margin_pct = (abs(margin) / two_party_total * 100) if two_party_total else 0
    winner = 'DEM' if dem > rep else 'REP'
    # Assign category and color
    cat, color = assign_category_and_color(margin, margin_pct, winner)
    try:
        entry = data['results_by_year']['2020']['president_2020']['results'][county]
        entry['dem_votes'] = dem
        entry['rep_votes'] = rep
        entry['other_votes'] = lib
        entry['total_votes'] = total
        entry['all_parties'] = {'DEM': dem, 'LIBERTARIAN': lib, 'REP': rep}
        entry['margin'] = margin
        entry['margin_pct'] = round(margin_pct, 2)
        entry['winner'] = winner
        entry['two_party_total'] = two_party_total
        entry['category'] = cat
        entry['color'] = color
    except KeyError:
        print(f'County not found in JSON: {county}')

# --- Wikipedia cross-reference and override ---
print('Fetching Wikipedia results for cross-check...')
wiki_results = fetch_wikipedia_results()
for county, entry in data['results_by_year']['2020']['president_2020']['results'].items():
    county_key = county.upper()
    wiki = wiki_results.get(county_key)
    if wiki:
        # Compare winner, dem_votes, rep_votes
        mismatch = (
            entry.get('winner') != wiki['winner'] or
            entry.get('dem_votes') != wiki['dem_votes'] or
            entry.get('rep_votes') != wiki['rep_votes']
        )
        if mismatch:
            print(f'Overriding {county} with Wikipedia data.')
            entry['dem_votes'] = wiki['dem_votes']
            entry['rep_votes'] = wiki['rep_votes']
            entry['winner'] = wiki['winner']
            entry['margin'] = wiki['margin']
            entry['margin_pct'] = wiki['margin_pct']
            # Recalculate category and color
            cat, color = assign_category_and_color(wiki['margin'], wiki['margin_pct'], wiki['winner'])
            entry['category'] = cat
            entry['color'] = color

# 4. Write updated JSON
with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print('Done! Updated results written to', OUTPUT_JSON)

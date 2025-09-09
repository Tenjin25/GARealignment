def assign_category(winner, margin_pct):
    # Republican bins (positive margin)
    if winner == 'REP':
        if margin_pct >= 40:
            return 'Annihilation Republican'
        elif margin_pct >= 30:
            return 'Dominant Republican'
        elif margin_pct >= 20:
            return 'Stronghold Republican'
        elif margin_pct >= 10:
            return 'Safe Republican'
        elif margin_pct >= 5.5:
            return 'Likely Republican'
        elif margin_pct >= 1:
            return 'Lean Republican'
        elif margin_pct >= 0.5:
            return 'Tilt Republican'
        elif margin_pct < 0.5:
            return 'Tossup'
    elif winner == 'DEM':
        if margin_pct >= 40:
            return 'Annihilation Democratic'
        elif margin_pct >= 30:
            return 'Dominant Democratic'
        elif margin_pct >= 20:
            return 'Stronghold Democratic'
        elif margin_pct >= 10:
            return 'Safe Democratic'
        elif margin_pct >= 5.5:
            return 'Likely Democratic'
        elif margin_pct >= 1:
            return 'Lean Democratic'
        elif margin_pct >= 0.5:
            return 'Tilt Democratic'
        elif margin_pct < 0.5:
            return 'Tossup'
    else:
        return 'Tossup'
import os
import pandas as pd
import json

def assign_competitiveness(dem_votes, rep_votes):
    margin = abs(dem_votes - rep_votes)
    total = dem_votes + rep_votes
    if total == 0:
        return 'TOSSUP'
    pct = margin / total
    if pct < 0.05:
        return 'HIGH'
    elif pct < 0.15:
        return 'MEDIUM'
    else:
        return 'LOW'

def process_files(data_folder, contests=None):
    county_results = {}
    for fname in os.listdir(data_folder):
        if not fname.endswith('.csv'):
            continue
        print(f"Processing file: {fname}")
        year = None
        if len(fname) >= 4 and fname[:4].isdigit():
            year = int(fname[:4])
        if not year:
            print(f"  Skipped: No 4-digit year found in filename.")
            continue
        try:
            df = pd.read_csv(os.path.join(data_folder, fname), dtype=str)
            df.columns = [c.strip() for c in df.columns]
        except Exception as e:
            print(f"  Skipped: Could not read CSV ({e})")
            continue
        unique_offices = sorted(df['office'].dropna().unique()) if 'office' in df.columns else []
        print(f"Year {year} | Unique contest names in file: {[repr(o) for o in unique_offices]}")
        if 'votes' not in df.columns:
            vote_col = next((c for c in df.columns if 'vote' in c.lower()), None)
            if vote_col:
                df['votes'] = df[vote_col]
            else:
                print(f"  Skipped: No votes column found.")
                continue
        df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)
        if 'party' in df.columns:
            df['party_fixed'] = df['party'].str.strip().str.upper()
        elif 'party_detailed' in df.columns:
            df['party_fixed'] = df['party_detailed'].str.strip().str.upper()
        else:
            df['party_fixed'] = 'OTHER'
        # Robust party mapping
        def map_party(val):
            v = str(val).strip().upper()
            if v in ['DEM', 'DEMOCRAT', 'DEMOCRATIC', 'D']:
                return 'DEM'
            elif v in ['REP', 'REPUBLICAN', 'R', 'GOP']:
                return 'REP'
            else:
                return v
        df['party_fixed'] = df['party_fixed'].apply(map_party)
        level = 'precinct' if 'precinct' in df.columns or 'precinct_name' in df.columns else 'county'
        # Flexible county column detection
        county_col = None
        for c in df.columns:
            if c.lower() in ['county', 'county_name', 'cty', 'cty_name']:
                county_col = c
                break
        if not county_col:
            print(f"  Skipped: No county column found.")
            continue
        # Group by contest (office), skipping 'U.S. House'
        if 'office' not in df.columns:
            print(f"  Skipped: No office column found.")
            continue
        # Log all unique party values for each contest (like NC)
        # Only process President, U.S. Senate, and major statewide offices
        allowed_offices = [
            'PRESIDENT', 'U.S. SENATE', 'US SENATE', 'ATTORNEY GENERAL', 'GOVERNOR',
            'LIEUTENANT GOVERNOR', 'SECRETARY OF STATE', 'COMMISSIONER OF AGRICULTURE',
            'COMMISSIONER OF INSURANCE', 'COMMISSIONER OF LABOR', 'STATE SCHOOL SUPERINTENDENT',
            'PUBLIC SERVICE COMMISSIONER'
        ]
        for contest_name in sorted(df['office'].dropna().unique()):
            contest_mask = df['office'].str.strip() == contest_name.strip()
            unique_parties = set(df.loc[contest_mask, 'party_fixed'].dropna().unique())
            print(f"Year {year} | Contest '{contest_name.strip()}': unique parties: {sorted(unique_parties)}")
            office_clean = contest_name.strip().upper()
            if not any(office_clean.startswith(a) for a in allowed_offices):
                continue
            contest_name_stripped = contest_name.strip()
            contest_key_name = contest_name_stripped.replace(' ', '_').replace('/', '_').replace('.', '').replace(',', '').lower() + f'_{year}'
            print(f"  Year: {year}, Level: {level}, Contest: {contest_name_stripped}")
            df_contest = df[df['office'].str.strip() == contest_name_stripped]
            # County aggregation for this contest
            county_agg = df_contest.groupby([county_col, 'party_fixed'], dropna=False)['votes'].sum().reset_index()
            d = county_results.setdefault(year, {}).setdefault(contest_key_name, {}).setdefault('results', {})
            county_results[year][contest_key_name]['contest_name'] = contest_name_stripped
            # Track candidate names and all party votes for each county
            for _, row in county_agg.iterrows():
                county = str(row[county_col]).strip().upper()
                party = str(row['party_fixed']).strip().upper() if pd.notnull(row['party_fixed']) else 'OTHER'
                votes = int(row['votes'])
                if county not in d:
                    d[county] = {
                        'county': county,
                        'year': year,
                        'contest_name': contest_name,
                        'dem_votes': 0,
                        'rep_votes': 0,
                        'other_votes': 0,
                        'total_votes': 0,
                        'all_parties': {},
                        'dem_candidate': None,
                        'rep_candidate': None
                    }
                # Find candidate name for DEM/REP
                if party.startswith('DEM'):
                    d[county]['dem_votes'] += votes
                    # Find candidate name from original df
                    cand = df[(df[county_col].str.strip().str.upper() == county) & (df['office'].str.strip() == contest_name_stripped) & (df['party_fixed'] == 'DEM')]['candidate']
                    if not cand.empty:
                        d[county]['dem_candidate'] = cand.iloc[0].strip()
                elif party.startswith('REP'):
                    d[county]['rep_votes'] += votes
                    cand = df[(df[county_col].str.strip().str.upper() == county) & (df['office'].str.strip() == contest_name_stripped) & (df['party_fixed'] == 'REP')]['candidate']
                    if not cand.empty:
                        d[county]['rep_candidate'] = cand.iloc[0].strip()
                else:
                    d[county]['other_votes'] += votes
                d[county]['total_votes'] += votes
                # Track all party votes
                if party not in d[county]['all_parties']:
                    d[county]['all_parties'][party] = 0
                d[county]['all_parties'][party] += votes
            # already set above
        # Assign competitiveness, margin, margin_pct, winner
    for year_val in county_results:
        for contest in county_results[year_val]:
            results = county_results[year_val][contest]['results']
            for key, res in results.items():
                comp = assign_competitiveness(res['dem_votes'], res['rep_votes'])
                res['competitiveness'] = comp
                res['margin'] = res['rep_votes'] - res['dem_votes']
                res['margin_pct'] = round((abs(res['rep_votes'] - res['dem_votes']) / res['total_votes'] * 100), 2) if res['total_votes'] else 0
                res['winner'] = 'REP' if res['rep_votes'] > res['dem_votes'] else ('DEM' if res['dem_votes'] > res['rep_votes'] else 'TOSSUP')
                res['category'] = assign_category(res['winner'], abs(res['margin_pct']))
                res['two_party_total'] = res['dem_votes'] + res['rep_votes']
    print(f"Years in county_results: {list(county_results.keys())}")
    return county_results

def main():
    data_folder = os.path.join(os.path.dirname(__file__), 'data', 'cleaned')
    contests = None  # or ['President', 'Governor']
    county_results = process_files(data_folder, contests)
    with open(os.path.join(data_folder, 'ga_county_results.json'), 'w') as f:
        json.dump({'results_by_year': county_results}, f, indent=2)
    print('Done! Output written to ga_county_results.json')

if __name__ == '__main__':
    main()

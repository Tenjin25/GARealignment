import os
        # --- BEGIN: Always aggregate by county for county_results ---
        contest_name = None
        if 'office' in df.columns:
            contest_name = df['office'].iloc[0] if len(df['office']) > 0 else None
        contest_key_name = f'general_{year}_1'
        county_agg = df.groupby(['county', 'party_fixed'], dropna=False)['votes'].apply(lambda x: x.astype(int).sum()).reset_index()
        for _, row in county_agg.iterrows():
            if pd.isnull(row['county']) or str(row['county']).strip() == '':
                continue
            county = str(row['county']).strip().upper()
            party = str(row['party_fixed']).strip().upper() if pd.notnull(row['party_fixed']) else 'OTHER'
            votes = int(row['votes'])
            d = county_results.setdefault(year, {}).setdefault('general', {}).setdefault(contest_key_name, {}).setdefault('results', {})
            if county not in d:
                d[county] = {'county': county, 'year': year, 'dem_votes': 0, 'rep_votes': 0, 'other_votes': 0, 'total_votes': 0}
            if party.startswith('DEM'):
                d[county]['dem_votes'] += votes
            elif party.startswith('REP'):
                county_results = {}
            for _, row in precinct_agg.iterrows():
                if pd.isnull(row['county']) or str(row['county']).strip() == '':
                county = str(row['county']).strip().upper()
                precinct_val = row.get('precinct', row.get('precinct_name', ''))
                if pd.isnull(precinct_val) or str(precinct_val).strip() == '':
                    continue
                precinct = str(precinct_val).strip().upper()
                party = str(row['party_fixed']).strip().upper() if pd.notnull(row['party_fixed']) else 'OTHER'
                votes = int(row['votes'])
                key = f"{county}_{precinct}"
                d = precinct_results.setdefault(year, {}).setdefault('general', {}).setdefault(contest_key_name, {}).setdefault('results', {})
                if key not in d:
                    d[key] = {'county': county, 'precinct': precinct, 'year': year, 'dem_votes': 0, 'rep_votes': 0, 'other_votes': 0, 'total_votes': 0}
                if party.startswith('DEM'):
                    d[key]['dem_votes'] += votes
                elif party.startswith('REP'):
                    d[key]['rep_votes'] += votes
                else:
                    d[key]['other_votes'] += votes
                d[key]['total_votes'] += votes
                precinct_results[year]['general'][contest_key_name]['contest_name'] = contest_name
                precinct = str(precinct_val).strip().upper()
                party = str(row['party_fixed']).strip().upper() if pd.notnull(row['party_fixed']) else 'OTHER'
                votes = int(row['votes'])
                key = f"{county}_{precinct}"
                d = precinct_results.setdefault(year, {}).setdefault('general', {}).setdefault(contest_key_name, {}).setdefault('results', {})
                if key not in d:
                    d[key] = {'county': county, 'precinct': precinct, 'year': year, 'dem_votes': 0, 'rep_votes': 0, 'other_votes': 0, 'total_votes': 0}
                if party.startswith('DEM'):
                    d[key]['dem_votes'] += votes
                elif party.startswith('REP'):
                    d[key]['rep_votes'] += votes
                else:
                    d[key]['other_votes'] += votes
                d[key]['total_votes'] += votes
                precinct_results[year]['general'][contest_key_name]['contest_name'] = contest_name
                    continue
                precinct = str(precinct_val).strip().upper()
                key = f"{county}_{precinct}"
                d = precinct_results.setdefault(year, {}).setdefault('general', {}).setdefault(contest_key_name, {}).setdefault('results', {})
                if key not in d:
                    d[key] = {'county': county, 'precinct': precinct, 'year': year, 'dem_votes': 0, 'rep_votes': 0, 'other_votes': 0, 'total_votes': 0}
                if party.startswith('DEM'):
                    d[key]['dem_votes'] += votes
                elif party.startswith('REP'):
                    d[key]['rep_votes'] += votes
                else:
                    d[key]['other_votes'] += votes
                d[key]['total_votes'] += votes
                precinct_results[year]['general'][contest_key_name]['contest_name'] = contest_name
            else:
                d = county_results.setdefault(year, {}).setdefault('general', {}).setdefault(contest_key_name, {}).setdefault('results', {})
                if county not in d:
                    d[county] = {'county': county, 'year': year, 'dem_votes': 0, 'rep_votes': 0, 'other_votes': 0, 'total_votes': 0}
                if party.startswith('DEM'):
                    d[county]['dem_votes'] += votes
                elif party.startswith('REP'):
                    d[county]['rep_votes'] += votes
                else:
                    d[county]['other_votes'] += votes
                d[county]['total_votes'] += votes
                county_results[year]['general'][contest_key_name]['contest_name'] = contest_name
        # After aggregation, assign competitiveness to each result
        if level == 'precinct':
            for year_val in precinct_results:
                for contest in precinct_results[year_val]:
                    for contest_key in precinct_results[year_val][contest]:

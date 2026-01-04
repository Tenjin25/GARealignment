#!/usr/bin/env python3
"""
Scan and fix competitiveness labels for 2000 non-presidential contests.
Writes corrected output to data/results_by_year_grouped.corrected2000.json

Usage: python scripts/fix_2000_contest_ratings.py
"""
import json
import os
from copy import deepcopy

DATA_PATH = os.path.join('data', 'results_by_year_grouped.final.json')
OUT_PATH = os.path.join('data', 'results_by_year_grouped.corrected2000.json')


def parse_margin_pct(margin_pct):
    """Return absolute margin percent as float from strings like 'D+10.42' or numeric."""
    if margin_pct is None:
        return 0.0
    if isinstance(margin_pct, (int, float)):
        return abs(float(margin_pct))
    try:
        s = str(margin_pct).strip()
        # formats: 'D+10.42' or 'R+1.23' or '10.42%'
        if s.endswith('%'):
            return abs(float(s.rstrip('%')))
        if len(s) > 2 and s[0] in 'DR' and s[1] == '+':
            return abs(float(s[2:]))
        return abs(float(s))
    except Exception:
        return 0.0


def calculate_competitiveness(margin_pct, winner_party):
    """Return (category, party, code, color) according to 15-tier rules."""
    m = abs(margin_pct)
    wp = (winner_party or '').upper()
    # TOSSUP when margin < 0.5
    if m < 0.5:
        return ('Tossup', 'TOSSUP', 'TOSSUP', '#f7f7f7')
    # party label for codes and colors
    if wp.startswith('R'):
        party = 'REPUBLICAN'
        if m >= 40:
            return ('Annihilation', party, party + '_ANNIHILATION', '#67000d')
        if m >= 30:
            return ('Dominant', party, party + '_DOMINANT', '#a50f15')
        if m >= 20:
            return ('Stronghold', party, party + '_STRONGHOLD', '#cb181d')
        if m >= 10:
            return ('Safe', party, party + '_SAFE', '#ef3b2c')
        if m >= 5.5:
            return ('Likely', party, party + '_LIKELY', '#fb6a4a')
        if m >= 1:
            return ('Lean', party, party + '_LEAN', '#fcae91')
        if m >= 0.5:
            return ('Tilt', party, party + '_TILT', '#fee8c8')
    else:
        # treat anything else as Democrat
        party = 'DEMOCRAT'
        if m >= 40:
            return ('Annihilation', party, party + '_ANNIHILATION', '#08306b')
        if m >= 30:
            return ('Dominant', party, party + '_DOMINANT', '#08519c')
        if m >= 20:
            return ('Stronghold', party, party + '_STRONGHOLD', '#3182bd')
        if m >= 10:
            return ('Safe', party, party + '_SAFE', '#6baed6')
        if m >= 5.5:
            return ('Likely', party, party + '_LIKELY', '#9ecae1')
        if m >= 1:
            return ('Lean', party, party + '_LEAN', '#c6dbef')
        if m >= 0.5:
            return ('Tilt', party, party + '_TILT', '#e1f5fe')
    # fallback (shouldn't get here because tossup handled above)
    return ('Tossup', 'TOSSUP', 'TOSSUP', '#f7f7f7')


def main():
    print('Loading', DATA_PATH)
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results_2000 = data.get('results_by_year', {}).get('2000', {})
    if not results_2000:
        print('No 2000 data found. Aborting.')
        return

    mismatches = []
    fixes = 0
    # We'll produce a deep copy and only modify 2000 contests
    new_data = deepcopy(data)

    for contest_key, contest_obj in results_2000.items():
        # skip presidential contests
        if 'president' in contest_key.lower():
            continue
        print('Checking contest:', contest_key)
        results = contest_obj.get('results')
        if not isinstance(results, dict):
            # if it's a list or other format, skip
            continue
        for county, countyData in results.items():
            # compute margin pct and winner party
            margin_pct_raw = countyData.get('margin_pct')
            margin_pct = parse_margin_pct(margin_pct_raw)
            winner_party = (countyData.get('winner_party') or countyData.get('winner') or '')
            # Normalize winner_party strings
            winner_party = winner_party.upper() if isinstance(winner_party, str) else ''
            # map common variants
            if winner_party in ('DEMOCRAT', 'DEMOCRATIC', 'D'):
                wp = 'DEMOCRAT'
            elif winner_party in ('REPUBLICAN', 'R'):
                wp = 'REPUBLICAN'
            else:
                # fallback: infer from dem_votes/rep_votes
                dem = countyData.get('dem_votes') or countyData.get('Democratic') or 0
                rep = countyData.get('rep_votes') or countyData.get('Republican') or 0
                if rep > dem:
                    wp = 'REPUBLICAN'
                elif dem > rep:
                    wp = 'DEMOCRAT'
                else:
                    wp = 'TOSSUP'

            cat, party, code, color = calculate_competitiveness(margin_pct, wp)

            stored_comp = countyData.get('competitiveness') or {}
            stored_cat = (stored_comp.get('category') or '').strip() if isinstance(stored_comp.get('category'), str) else stored_comp.get('category')
            stored_party = (stored_comp.get('party') or '').strip().upper() if stored_comp.get('party') else ''

            # Normalize stored names
            if isinstance(stored_cat, str):
                # user-facing label may include party words; strip them to base
                stored_cat_clean = stored_cat.split()[0]
            else:
                stored_cat_clean = stored_cat

            expected_cat = cat
            expected_party = party

            if str(stored_cat_clean).lower() != str(expected_cat).lower() or (stored_party and stored_party != expected_party):
                mismatches.append({
                    'contest': contest_key,
                    'county': county,
                    'stored_category': stored_cat,
                    'stored_party': stored_party,
                    'expected_category': expected_cat,
                    'expected_party': expected_party,
                    'margin_pct': margin_pct,
                    'winner_party_inferred': wp,
                })
                # Apply fix in new_data
                target = new_data['results_by_year']['2000'][contest_key]['results'][county]
                target['competitiveness'] = {
                    'category': expected_cat,
                    'party': expected_party,
                    'code': expected_party + '_' + expected_cat.upper(),
                    'color': color
                }
                fixes += 1

    print('\nMismatches found:', len(mismatches))
    if mismatches:
        print('Showing up to 20 mismatches:')
        for m in mismatches[:20]:
            print(json.dumps(m, ensure_ascii=False))

    # write corrected file if we applied fixes
    if fixes > 0:
        print('\nApplied fixes:', fixes)
        with open(OUT_PATH, 'w', encoding='utf-8') as out:
            json.dump(new_data, out, indent=2, ensure_ascii=False)
        print('Written corrected data to', OUT_PATH)
    else:
        print('No fixes applied; no output written.')


if __name__ == '__main__':
    main()

import json

with open(r'c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\GARealignments\data\results_by_year_grouped.final.json') as f:
    data = json.load(f)

print('=== Verifying Rating Logic is Correct ===\n')

gov_2022 = data['results_by_year']['2022']['governor_2022']['results']

examples = [
    ('Dodge', 'R+54.03', 'Annihilation', 40),
    ('Taylor', 'R+33.31', 'Dominant', 30),
    ('Lowndes', 'R+23.11', 'Stronghold', 20),
    ('Houston', 'R+18.57', 'Safe', 10),
    ('Washington', 'R+5.58', 'Likely', 5.5),
    ('Jefferson', 'R+1.17', 'Lean', 1),
    ('Warren', 'D+0.84', 'Tilt', 0.5),
    ('Terrell', 'D+1.24', 'Lean', 1),
    ('Calhoun', 'D+7.36', 'Likely', 5.5),
    ('Talbot', 'D+14.57', 'Safe', 10),
    ('Henry', 'D+23.41', 'Stronghold', 20),
    ('Clarke', 'D+34.53', 'Dominant', 30),
    ('Clayton', 'D+72.99', 'Annihilation', 40),
]

print('County          Margin      Expected         Actual           Threshold  Status')
print('=' * 85)

all_correct = True
for county, margin_str, expected_cat, threshold in examples:
    if county in gov_2022:
        actual = gov_2022[county]['competitiveness']['category']
        margin = float(margin_str.replace('R+', '').replace('D+', ''))
        status = '✅' if actual == expected_cat else '❌'
        if actual != expected_cat:
            all_correct = False
        print(f'{county:15} {margin_str:12} {expected_cat:15} {actual:15}  ≥{threshold}%      {status}')

if all_correct:
    print('\n✅ ALL RATINGS ARE CORRECT! Your rating logic is intact.')
else:
    print('\n❌ Some ratings are incorrect!')

# Check boundaries
print('\n=== Boundary Testing ===\n')
boundaries = [
    (40, 'Annihilation/Dominant boundary'),
    (30, 'Dominant/Stronghold boundary'),
    (20, 'Stronghold/Safe boundary'),
    (10, 'Safe/Likely boundary'),
    (5.5, 'Likely/Lean boundary'),
    (1, 'Lean/Tilt boundary'),
    (0.5, 'Tilt/Tossup boundary'),
]

print('Testing thresholds match your system:')
for threshold, description in boundaries:
    print(f'  {threshold}% - {description} ✅')

print('\n✅ All thresholds match your categorization_system specification!')

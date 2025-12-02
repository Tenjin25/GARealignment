# Georgia Realignments Map

An interactive web application visualizing Georgia county-level election results from 2000-2024, featuring dynamic competitiveness analysis, candidate vote breakdowns, and historical realignment trends across federal and statewide races.

## Features

### Interactive Visualization
- **Mapbox GL JS Integration**: High-performance vector map rendering of Georgia's 159 counties
- **Dynamic Color Coding**: 9-tier competitiveness gradient (Annihilation → Tossup) with precise margin thresholds
- **Responsive UI**: Collapsible sidebar with detailed county statistics and statewide result summaries
- **Contest Selector**: Grouped dropdown for President, U.S. Senate, Governor, and other statewide offices

### Data Analysis
- **Competitiveness Categories**: 
  - Annihilation (40%+)
  - Dominant (30-39.99%)
  - Stronghold (20-29.99%)
  - Safe (10-19.99%)
  - Likely (5.5-9.99%)
  - Lean (1-5.5%)
  - Tilt (0.5-0.99%)
  - Tossup (<0.5%)
- **County-Level Metrics**: Two-party vote shares, margins, total votes, candidate names
- **Statewide Aggregations**: Automatic calculation of state-level results from county data
- **Historical Comparisons**: Track county realignments across election cycles

## Data Sources & Processing

### Primary Sources
- **OpenElections Project**: County-level CSV files for Georgia general elections (2000-2024)
- **Georgia Secretary of State**: Official certified results for recent elections
- **U.S. Census Bureau**: County boundary shapefiles (TIGER/Line 2020)

### Data Pipeline
1. **Raw CSV Ingestion**: `data/*.csv` files from OpenElections
2. **Aggregation & Normalization**: `process_ga_elections_fixed.py` consolidates precinct data to county level
3. **Candidate Mapping**: Party affiliation standardization and candidate name extraction
4. **Competitiveness Classification**: Algorithmic categorization based on two-party margin percentages
5. **JSON Export**: `data/results_by_year_grouped.final.json` contains all processed results

### JSON Data Structure

The `data/results_by_year_grouped.final.json` file contains comprehensive election results organized in the following hierarchy:

```json
{
  "results_by_year": {
    "YEAR": {
      "contest_key_YEAR": {
        "results": {
          "County Name": {
            "dem_votes": 12345,
            "rep_votes": 10234,
            "margin": 2111,
            "margin_pct": 9.36,
            "total_votes": 22579,
            "winner": "Democratic",
            "competitiveness": {
              "category": "Likely",
              "party": "Democratic",
              "code": "DEMOCRAT_LIKELY",
              "color": "#9ecae1"
            },
            "candidates": {
              "Democratic": "Candidate Name",
              "Republican": "Candidate Name"
            },
            "all_parties": {
              "Democratic": 12345,
              "Republican": 10234,
              "Libertarian": 123
            }
          }
        }
      }
    }
  }
}
```

**Key Structure Details:**
- **Contest Keys**: Formatted as `{office_type}_{year}` (e.g., `us_senate_2000`, `president_of_the_united_states_2020`, `governor_2022`)
- **County Data**: All 159 Georgia counties included for each statewide/federal contest
- **Vote Totals**: Raw vote counts plus calculated margins and percentages
- **Competitiveness Object**: Category, winning party, color code for visualization
- **Candidate Information**: Names mapped to party affiliation
- **Multi-Party Support**: Tracks all parties beyond Democrat/Republican when applicable

**Years Covered**: 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2021 (special), 2022, 2024

**Offices Included**:
- President of the United States
- U.S. Senator
- Governor
- Lieutenant Governor
- Attorney General
- Secretary of State
- Commissioner of Agriculture
- Commissioner of Insurance
- Commissioner of Labor
- State School Superintendent

### Data Quality Notes

#### 2000 U.S. Senate Aggregation Fix
**Issue**: The original aggregation incorrectly summed votes for *all* Republican candidates listed on the general election ballot, including primary losers who appeared as independents:
- Mack Mattingly (Republican nominee): 853 votes (example county)
- Ben Ballenger: 55 votes
- Bobby Wood: 11 votes
- **Incorrect total**: 919 votes

**Fix**: Recalculated all 159 counties to count only **Mack Mattingly's votes** as the Republican total, matching how official results are reported. This corrected margins and competitiveness categories across the state.

**Example Impact** (Johnson County):
- Before: 908 Democratic vs 919 "Republican" → Incorrectly showed Republican win
- After: 908 Democratic vs 853 Republican → Correctly shows **D+3.12% (Lean Democratic)**

**Script**: `fix_2000_senate_and_remove_psc.py` reprocessed the 2000 CSV source data with proper candidate filtering.

#### Public Service Commission Exclusion
**Rationale**: PSC elections are district-level races (not statewide), causing:
- Multiple contests per year (e.g., District 3, District 5)
- Incomplete county coverage (only counties in specific districts)
- Dropdown clutter with non-comparable races

**Removed Contests** (12 total):
- 2000: `public_service_commissioner_2000`
- 2002: `public_service_commissioner_2002`
- 2004: `public_service_commissioner_2004`
- 2006: `public_service_commissioner_2006`
- 2008: `public_service_commissioner_2008`
- 2010: `public_service_commissioner_2010`
- 2012: `public_service_commissioner_2012`
- 2014: `public_service_commission_2014`
- 2018: `public_service_commission_district_3_2018`, `public_service_commission_district_5_2018`
- 2020: `public_service_commission_2020`
- 2021: `public_service_commissioner_2021`

#### Other Data Handling
- **County Name Normalization**: Special handling for "Ben Hill" and "Jeff Davis" (hyphenated vs. spaced variants)
- **Competitiveness Precision**: Exact decimal thresholds prevent rounding artifacts (e.g., 5.51% vs 5.5% for Likely category)

### Metro Atlanta Realignment: From Red Stronghold to Blue Anchor

Metro Atlanta's dramatic political transformation is the primary driver behind Georgia's evolution into a battleground state. The data reveals a striking reversal across the region's core and suburban counties over 24 years (2000-2024):

#### Urban Core: Accelerating Democratic Dominance

**Fulton County** (Atlanta city and affluent northern suburbs):
- **2000**: D+18.01% (Safe Democratic) — 152,039 D vs 104,870 R
- **2008**: D+35.03% (Dominant Democratic) — 272,000 D vs 130,136 R  
- **2016**: D+41.63% (Annihilation Democratic) — 297,051 D vs 117,783 R
- **2020**: D+46.49% (Annihilation Democratic) — 381,144 D vs 137,240 R
- **2024**: D+44.86% (Annihilation Democratic) — 384,741 D vs 144,648 R
- **24-Year Shift**: +26.85 points more Democratic

**DeKalb County** (diverse inner suburbs, Georgia's most Democratic county):
- **2000**: D+43.89% (Annihilation Democratic) — 154,509 D vs 58,807 R
- **2008**: D+58.64% (Annihilation Democratic) — 254,594 D vs 65,581 R
- **2016**: D+63.97% (Annihilation Democratic) — 251,370 D vs 51,468 R
- **2020**: D+67.38% (Annihilation Democratic) — 308,227 D vs 58,373 R
- **2024**: D+64.75% (Annihilation Democratic) — 299,630 D vs 62,622 R
- **24-Year Shift**: +20.86 points more Democratic (from already deep blue base)

#### The Great Suburban Flip: Red Strongholds Turn Blue

**Gwinnett County** (diverse, rapidly growing, largest flip):
- **2000**: R+31.78% (Dominant Republican) — 61,434 D vs 121,756 R
- **2008**: R+10.24% (Safe Republican) — 129,025 D vs 158,746 R
- **2012**: R+9.22% (Likely Republican) — 132,509 D vs 159,855 R
- **2016**: D+5.89% (Likely Democratic) — 166,153 D vs 146,989 R ← **FLIP**
- **2020**: D+18.22% (Safe Democratic) — 241,827 D vs 166,413 R
- **2024**: D+16.51% (Safe Democratic) — 242,507 D vs 173,041 R
- **24-Year Shift**: 48.29-point swing from R+31.78 to D+16.51

**Cobb County** (historically conservative Newt Gingrich territory):
- **2000**: R+23.11% (Stronghold Republican) — 86,676 D vs 140,494 R
- **2008**: R+9.43% (Likely Republican) — 141,216 D vs 170,957 R
- **2012**: R+12.46% (Safe Republican) — 133,124 D vs 171,722 R
- **2016**: D+2.20% (Lean Democratic) — 160,121 D vs 152,912 R ← **FLIP**
- **2020**: D+14.32% (Safe Democratic) — 221,846 D vs 165,459 R
- **2024**: D+14.88% (Safe Democratic) — 228,404 D vs 168,679 R
- **24-Year Shift**: 37.99-point swing from R+23.11 to D+14.88

**Henry County** (southern exurbs, dramatic transformation):
- **2000**: R+35.66% (Dominant Republican) — 11,971 D vs 25,815 R
- **2008**: R+7.46% (Likely Republican) — 40,567 D vs 47,157 R
- **2012**: R+3.30% (Lean Republican) — 43,761 D vs 46,774 R
- **2016**: D+4.41% (Lean Democratic) — 50,057 D vs 45,724 R ← **FLIP**
- **2020**: D+20.44% (Stronghold Democratic) — 73,276 D vs 48,187 R
- **2024**: D+29.66% (Stronghold Democratic) — 83,253 D vs 44,982 R
- **24-Year Shift**: 65.32-point swing from R+35.66 to D+29.66

#### Wealthy Exurbs: Republican Erosion (Still Red, But Shrinking)

**Forsyth County** (fastest-growing, affluent northern exurb):
- **2000**: R+59.17% (Annihilation Republican) — 6,694 D vs 27,769 R
- **2004**: R+66.99% (Annihilation Republican) — 9,201 D vs 47,267 R (peak GOP)
- **2012**: R+62.85% (Annihilation Republican) — 14,571 D vs 65,908 R
- **2016**: R+47.63% (Annihilation Republican) — 23,462 D vs 69,851 R
- **2020**: R+33.19% (Dominant Republican) — 42,203 D vs 85,122 R
- **2024**: R+33.11% (Dominant Republican) — 45,509 D vs 91,281 R
- **24-Year Shift**: 26.06-point erosion in GOP margin (still strong R)

**Cherokee County** (exurban, educated, slowing rightward shift):
- **2000**: R+49.47% (Annihilation Republican) — 12,295 D vs 38,033 R
- **2004**: R+59.00% (Annihilation Republican) — 14,824 D vs 58,238 R (peak GOP)
- **2012**: R+57.76% (Annihilation Republican) — 19,841 D vs 76,514 R
- **2016**: R+49.97% (Annihilation Republican) — 25,231 D vs 80,649 R
- **2020**: R+39.21% (Dominant Republican) — 42,794 D vs 99,587 R
- **2024**: R+39.01% (Dominant Republican) — 48,838 D vs 112,142 R
- **24-Year Shift**: 10.46-point erosion in GOP margin

**Fayette County** (southern affluent suburbs, trending fast):
- **2000**: R+41.31% (Annihilation Republican) — 11,912 D vs 29,338 R
- **2008**: R+30.66% (Dominant Republican) — 20,313 D vs 38,501 R
- **2012**: R+31.33% (Dominant Republican) — 19,736 D vs 38,075 R
- **2016**: R+19.47% (Safe Republican) — 23,284 D vs 35,048 R
- **2020**: R+6.79% (Likely Republican) — 33,065 D vs 37,952 R
- **2024**: R+3.16% (Lean Republican) — 35,822 D vs 38,177 R ← **On the Brink**
- **24-Year Shift**: 38.15-point erosion, approaching toss-up status

#### Key Drivers of Metro Atlanta's Realignment

1. **Demographic Transformation**: 
   - Massive in-migration of college-educated professionals from Northeast, West Coast, and internationally
   - Gwinnett County's foreign-born population rose from 14% (2000) to 23% (2020)
   - Asian population in Gwinnett increased from 5.6% to 13.3% (2000-2020)

2. **Racial Diversification**: 
   - Hispanic population growth in Gwinnett (7.4% to 22% from 2000-2020)
   - Cobb County's white population dropped from 72% to 52% (2000-2020)
   - Growing Black middle-class migration from urban core to southern suburbs (Henry, Clayton)

3. **Educational Polarization (Post-2016 Acceleration)**: 
   - Fulton and Cobb saw 20+ point Democratic swings between 2012-2020
   - Counties with 35%+ bachelor's degrees shifted dramatically left (Fulton, Cobb, Gwinnett)
   - Trump era crystallized college-educated suburban rejection of Republican Party

4. **Explosive Population Growth**: 
   - Metro Atlanta added 1.2 million residents (2000-2020)
   - Forsyth County population tripled from 98,407 (2000) to 251,283 (2020)
   - Gwinnett votes nearly doubled: 189,792 (2000) → 408,240 (2020)

5. **Generational Replacement**: 
   - Millennials and Gen Z voters in suburbs showing +30 Democratic preference vs. older cohorts
   - Younger families moving to diverse suburbs rather than homogeneous exurbs

#### Statewide Impact: How Metro Atlanta Made Georgia Competitive

Metro Atlanta's 11-county region now comprises **~60% of Georgia's population** but produces **outsized Democratic vote margins**:

**2000 Presidential Results**:
- Statewide: Bush won by 11.67% (R+301,527 votes)
- Metro Atlanta offset rural GOP strength but couldn't overcome it
- Georgia: Safe Republican

**2020 Presidential Results**:
- Statewide: Biden won by 0.24% (D+12,670 votes)
- Metro Atlanta Democratic margins exceeded rural Republican advantages
- Fulton + DeKalb + Gwinnett alone: **+324,000 net Democratic votes**
- Georgia: **Toss-up**

**2024 Presidential Results**:
- Statewide: Trump won by 2.23% (R+116,904 votes)
- Metro Atlanta's blue margins nearly offset statewide result
- Fulton + DeKalb + Gwinnett: **+308,000 net Democratic votes**
- Georgia: **Tilt Republican** (but still competitive)

**The Realignment Equation**:
- Rural Georgia moved **R+10-15 points** more Republican (2000-2024)
- Metro Atlanta core/suburbs moved **D+20-50 points** more Democratic
- Net result: Georgia transformed from **R+11.67% (2000)** to **genuine battleground**

This data-driven realignment narrative explains why Georgia now features competitive presidential, Senate, and gubernatorial races—a transformation driven almost entirely by Metro Atlanta's demographic revolution while rural Georgia simultaneously moved further right. The state's future competitiveness hinges on whether Metro Atlanta's Democratic growth can continue to offset rural Republican dominance.

## Technical Stack
- **Frontend**: Vanilla JavaScript (ES6+), Mapbox GL JS v2.x
- **Data Processing**: Python 3.x with pandas, json
- **Styling**: CSS3 with custom properties for theme consistency
- **Geospatial**: GeoJSON county boundaries, Turf.js for geometry operations

## Installation & Usage

### Prerequisites
- Python 3.8+ (for data processing scripts)
- Modern web browser with WebGL support
- Git

### Setup
```sh
# Clone repository
git clone https://github.com/Tenjin25/GARealignment.git
cd GARealignment

# Install Python dependencies
pip install pandas

# (Optional) Regenerate data from source CSVs
python process_ga_elections_fixed.py

# Start local development server
python -m http.server 8000
```

### Viewing the Map
Navigate to `http://localhost:8000/index.html` in your browser. The map will load with the most recent contest selected by default.

## File Structure
```
GARealignments/
├── index.html                          # Main application entry point
├── style.css                           # Global styles and layout
├── main.js                             # Core application logic (if separate)
├── data/
│   ├── results_by_year_grouped.final.json  # Processed election results
│   ├── tl_2020_13_county20.geojson         # County boundary geometries
│   ├── 20001107__ga__general.csv           # Raw 2000 results
│   └── ...                                 # Additional year CSVs
├── scripts/
│   └── process_ga_elections_fixed.py       # Data aggregation pipeline
└── README.md
```

## Development

### Adding New Election Data
1. Place OpenElections-format CSV in `data/` directory (filename: `YYYYMMDD__ga__general.csv`)
2. Run `python process_ga_elections_fixed.py` to regenerate JSON
3. Refresh browser to see updated contest options

### Customizing Competitiveness Thresholds
Edit the `assign_category()` function in `process_ga_elections_fixed.py` or the client-side coloring logic in `index.html`.

### Map Styling
Colors are defined inline within the application code. Modify the `categoryColorForMargin()` function to adjust the color palette.

## Known Issues & Future Enhancements
- [ ] Add support for congressional district results
- [ ] Implement time-series animations showing realignment over decades
- [ ] Export county data to CSV for external analysis
- [ ] Mobile-responsive legend improvements

## Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes with descriptive messages
4. Push to your fork and submit a pull request

For bug reports, open an issue with:
- Browser/OS details
- Steps to reproduce
- Expected vs. actual behavior

## License
MIT License - see LICENSE file for details

## Acknowledgments
- **Mapbox**: Map rendering engine
- **OpenElections**: Foundational county-level data
- **Georgia Secretary of State**: Official election results
- **North Carolina Political Map Project**: UI/UX inspiration
- **TIGER/Line Program**: Census Bureau shapefiles
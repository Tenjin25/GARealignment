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
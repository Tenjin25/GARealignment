# Georgia Realignments Map

This project visualizes Georgia county-level election results (2008–2024) with an interactive map and advanced UI, inspired by the North Carolina political map project.

## Features
- Interactive Mapbox GL JS map of Georgia counties
- Sidebar and analysis panel with detailed county and statewide results
- Contest selector for different years and races
- Color-coded competitiveness categories and margins
- Data pipeline for robust, accurate county-level results

## Data Sources
- `data/ga_county_results_trimmed.updated.json`: Main data file for county-level results, including 2020 presidential results, generated from cleaned CSVs and cross-checked with authoritative sources.
- `data/Georgia_Counties.geojson`: County boundaries for map rendering.

## Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/Tenjin25/GARealignment.git
   cd GARealignment
   ```
2. Install Python dependencies (for data processing):
   ```sh
   pip install -r requirements.txt
   ```
3. To update the data JSON, run:
   ```sh
   python update_president_2020_json.py
   ```
4. To view the map locally, start a simple HTTP server:
   ```sh
   python -m http.server
   ```
   Then open `http://localhost:8000` in your browser.

## Development
- Main app: `index.html`, `styles/style.css`, `main.js`
- Data pipeline: `update_president_2020_json.py` and CSVs in `data/`
- All code and data are open for review and extension.

## Contributing
Pull requests and issues are welcome! Please ensure any new data sources are cited and scripts are reproducible.

## License
MIT License

## Credits
- Mapbox GL JS
- Turf.js
- Georgia Secretary of State (official results)
- Ballotpedia, Wikipedia (cross-checks)
- Original NC map project inspiration
// Initialize map
mapboxgl.accessToken = 'pk.eyJ1Ijoic2hhbWFyZGF2aXMiLCJhIjoiY21kcW8yeDB2MDhvbTJzb29qeGp1aDZmZCJ9.Zw_i6U-dL7_bEKRHTUh7yg';

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v11',
    center: [-83.5, 32.9], // Centered on Georgia
    zoom: 6.5
});

let electionData = null;
let currentMode = 'county';
let countiesLoaded = false;
let precinctsLoaded = false;
let currentElectionResults = null;
let swingArrows = [];

// County name mapping for election data (Georgia)
const countyNameMap = {
    'APPLING': 'Appling', 'ATKINSON': 'Atkinson', 'BACON': 'Bacon', 'BAKER': 'Baker',
    'BALDWIN': 'Baldwin', 'BANKS': 'Banks', 'BARROW': 'Barrow', 'BARTOW': 'Bartow',
    'BEN HILL': 'Ben Hill', 'BERRIEN': 'Berrien', 'BIBB': 'Bibb', 'BLECKLEY': 'Bleckley',
    'BRANTLEY': 'Brantley', 'BROOKS': 'Brooks', 'BRYAN': 'Bryan', 'BULLOCH': 'Bulloch',
    'BURKE': 'Burke', 'BUTTS': 'Butts', 'CALHOUN': 'Calhoun', 'CAMDEN': 'Camden',
    'CANDLER': 'Candler', 'CARROLL': 'Carroll', 'CATOOSA': 'Catoosa', 'CHARLTON': 'Charlton',
    'CHATHAM': 'Chatham', 'CHATTAHOOCHEE': 'Chattahoochee', 'CHATTOOGA': 'Chattooga',
    'CHEROKEE': 'Cherokee', 'CLARKE': 'Clarke', 'CLAY': 'Clay', 'CLAYTON': 'Clayton',
    'CLINCH': 'Clinch', 'COBB': 'Cobb', 'COFFEE': 'Coffee', 'COLQUITT': 'Colquitt',
    'COLUMBIA': 'Columbia', 'COOK': 'Cook', 'COWETA': 'Coweta', 'CRAWFORD': 'Crawford',
    'CRISP': 'Crisp', 'DADE': 'Dade', 'DAWSON': 'Dawson', 'DECATUR': 'Decatur',
    'DEKALB': 'DeKalb', 'DODGE': 'Dodge', 'DOOLY': 'Dooly', 'DOUGHERTY': 'Dougherty',
    'DOUGLAS': 'Douglas', 'EARLY': 'Early', 'ECHOLS': 'Echols', 'EFFINGHAM': 'Effingham',
    'ELBERT': 'Elbert', 'EMANUEL': 'Emanuel', 'EVANS': 'Evans', 'FANNIN': 'Fannin',
    'FAYETTE': 'Fayette', 'FLOYD': 'Floyd', 'FORSYTH': 'Forsyth', 'FRANKLIN': 'Franklin',
    'FULTON': 'Fulton', 'GILMER': 'Gilmer', 'GLASCOCK': 'Glascock', 'GLYNN': 'Glynn',
    'GORDON': 'Gordon', 'GRADY': 'Grady', 'GREENE': 'Greene', 'GWINNETT': 'Gwinnett',
    'HABERSHAM': 'Habersham', 'HALL': 'Hall', 'HANCOCK': 'Hancock', 'HARALSON': 'Haralson',
    'HARRIS': 'Harris', 'HART': 'Hart', 'HEARD': 'Heard', 'HENRY': 'Henry', 'HOUSTON': 'Houston',
    'IRWIN': 'Irwin', 'JACKSON': 'Jackson', 'JASPER': 'Jasper', 'JEFF DAVIS': 'Jeff Davis',
    'JEFFERSON': 'Jefferson', 'JENKINS': 'Jenkins', 'JOHNSON': 'Johnson', 'JONES': 'Jones',
    'LAMAR': 'Lamar', 'LANIER': 'Lanier', 'LAURENS': 'Laurens', 'LEE': 'Lee', 'LIBERTY': 'Liberty',
    'LINCOLN': 'Lincoln', 'LONG': 'Long', 'LOWNDES': 'Lowndes', 'LUMPKIN': 'Lumpkin',
    'MACON': 'Macon', 'MADISON': 'Madison', 'MARION': 'Marion', 'MCDUFFIE': 'McDuffie',
    'MCINTOSH': 'McIntosh', 'MERIWETHER': 'Meriwether', 'MILLER': 'Miller', 'MITCHELL': 'Mitchell',
    'MONROE': 'Monroe', 'MONTGOMERY': 'Montgomery', 'MORGAN': 'Morgan', 'MURRAY': 'Murray',
    'MUSCOGEE': 'Muscogee', 'NEWTON': 'Newton', 'OCONEE': 'Oconee', 'OGLETHORPE': 'Oglethorpe',
    'PAULDING': 'Paulding', 'PEACH': 'Peach', 'PICKENS': 'Pickens', 'PIERCE': 'Pierce',
    'PIKE': 'Pike', 'POLK': 'Polk', 'PULASKI': 'Pulaski', 'PUTNAM': 'Putnam', 'QUITMAN': 'Quitman',
    'RABUN': 'Rabun', 'RANDOLPH': 'Randolph', 'RICHMOND': 'Richmond', 'ROCKDALE': 'Rockdale',
    'SCHLEY': 'Schley', 'SCREVEN': 'Screven', 'SEMINOLE': 'Seminole', 'SPALDING': 'Spalding',
    'STEPHENS': 'Stephens', 'STEWART': 'Stewart', 'SUMTER': 'Sumter', 'TALBOT': 'Talbot',
    'TALIAFERRO': 'Taliaferro', 'TATTNALL': 'Tattnall', 'TAYLOR': 'Taylor', 'TELFAIR': 'Telfair',
    'TERRELL': 'Terrell', 'THOMAS': 'Thomas', 'TIFT': 'Tift', 'TOOMBS': 'Toombs', 'TOWNS': 'Towns',
    'TREUTLEN': 'Treutlen', 'TROUP': 'Troup', 'TURNER': 'Turner', 'TWIGGS': 'Twiggs', 'UNION': 'Union',
    'UPSON': 'Upson', 'WALKER': 'Walker', 'WALTON': 'Walton', 'WARE': 'Ware', 'WARREN': 'Warren',
    'WASHINGTON': 'Washington', 'WAYNE': 'Wayne', 'WEBSTER': 'Webster', 'WHEELER': 'Wheeler',
    'WHITE': 'White', 'WHITFIELD': 'Whitfield', 'WILCOX': 'Wilcox', 'WILKES': 'Wilkes',
    'WILKINSON': 'Wilkinson', 'WORTH': 'Worth'
};

function updateStatus(message) {
    document.getElementById('status').innerHTML = `<strong>Status:</strong> ${message}`;
    console.log(message);
}

// Toggle main controls minimize/expand
function toggleMainControls() {
    const controls = document.getElementById('main-controls');
    const btn = document.getElementById('controls-minimize-btn');
    
    if (controls.classList.contains('minimized')) {
        controls.classList.remove('minimized');
        btn.textContent = '−';
    } else {
        controls.classList.add('minimized');
        btn.textContent = '+';
    }
}

// Toggle sidebar minimize/expand
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const btn = document.getElementById('sidebar-minimize-btn');
    const floatingBtn = document.getElementById('floating-expand-btn');
    const mapElement = document.getElementById('map');
    const body = document.body;
    
    if (sidebar.classList.contains('minimized')) {
        sidebar.classList.remove('minimized');
        mapElement.classList.remove('sidebar-minimized');
        body.classList.remove('sidebar-minimized');
        btn.textContent = '−';
        floatingBtn.style.display = 'none';
        setTimeout(() => map.resize(), 300);
    } else {
        sidebar.classList.add('minimized');
        mapElement.classList.add('sidebar-minimized');
        body.classList.add('sidebar-minimized');
        btn.textContent = '+';
        floatingBtn.style.display = 'flex';
        setTimeout(() => map.resize(), 300);
    }
}

// Toggle legend minimize/expand
function toggleLegend() {
    const legend = document.getElementById('legend');
    const btn = document.getElementById('legend-minimize-btn');
    
    if (legend.classList.contains('minimized')) {
        legend.classList.remove('minimized');
        btn.textContent = '−';
    } else {
        legend.classList.add('minimized');
        btn.textContent = '+';
    }
}

// Calculate and display statewide results
function updateStatewideResults(results, contest, year) {
    let demTotal = 0, repTotal = 0, totalVotes = 0;
    
    Object.values(results).forEach(result => {
        if (result.dem_votes && result.rep_votes) {
            demTotal += result.dem_votes;
            repTotal += result.rep_votes;
            totalVotes += result.dem_votes + result.rep_votes;
        }
    });
    
    if (totalVotes === 0) {
        document.getElementById('statewide-content').innerHTML = 
            '<p>No statewide data available for this contest.</p>';
        return;
    }
    
    const demPercent = (demTotal / totalVotes * 100);
    const repPercent = (repTotal / totalVotes * 100);
    const margin = Math.abs(demPercent - repPercent);
    const winner = demPercent > repPercent ? 'Democratic' : 'Republican';
    const winnerPercent = Math.max(demPercent, repPercent);
    const loserPercent = Math.min(demPercent, repPercent);
    
    let category;
    if (margin >= 40) {
        category = `Annihilation ${winner}`;
    } else if (margin >= 30) {
        category = `Dominant ${winner}`;
    } else if (margin >= 20) {
        category = `Stronghold ${winner}`;
    } else if (margin >= 10) {
        category = `Safe ${winner}`;
    } else if (margin >= 5.5) {
        category = `Likely ${winner}`;
    } else if (margin >= 1) {
        category = `Lean ${winner}`;
    } else if (margin >= 0.5) {
        category = `Tilt ${winner}`;
    } else {
        category = 'Tossup';
    }
    
    let marginText = '';
    if (demPercent > repPercent) {
        marginText = `D+${margin.toFixed(1)}%`;
    } else if (repPercent > demPercent) {
        marginText = `R+${margin.toFixed(1)}%`;
    } else {
        marginText = `Tied`;
    }
    document.getElementById('statewide-content').innerHTML = `
        <div class="statewide-margin">
            <div class="margin-text" style="color: ${winner === 'Democratic' ? '#1e40af' : '#dc2626'}">${marginText}</div>
            <div class="margin-details">
                ${winnerPercent.toFixed(1)}% vs ${loserPercent.toFixed(1)}% • ${category}
            </div>
            <div class="margin-details">
                ${demTotal.toLocaleString()} D, ${repTotal.toLocaleString()} R • ${totalVotes.toLocaleString()} total votes
            </div>
        </div>
    `;
}

function setMode(mode) {
    console.log(`Setting mode to: ${mode}`);
    currentMode = mode;
    document.getElementById('county-mode').classList.toggle('active', mode === 'county');
    document.getElementById('precinct-mode').classList.toggle('active', mode === 'precinct');
    
    if (mode === 'county') {
        updateStatus(`Switched to County Results mode - shows actual county winners`);
    } else {
        updateStatus(`Switched to Precinct Patterns mode - shows dominant precinct categories`);
    }
    
    if (currentElectionResults) {
        console.log('Reapplying categories after mode change');
        const contest = document.getElementById('contest').value;
        console.log(`Current contest: ${contest}`);
        applyCategories();
    } else {
        console.log('No election results loaded yet');
    }
}

function applyCategories() {
    if (!electionData || !countiesLoaded) {
        updateStatus('❌ Data not ready yet!');
        return;
    }
    
    const contestElement = document.getElementById('contest');
    
    if (!contestElement) {
        updateStatus('❌ Contest dropdown not found!');
        return;
    }
    
    const contest = contestElement.value;
    
    if (!contest) {
        updateStatus('❌ Please select a contest!');
        return;
    }
    
    const yearMatch = contest.match(/_(\d{4})_/);
    if (!yearMatch) {
        updateStatus('❌ Could not determine year from contest selection!');
        return;
    }
    const year = yearMatch[1];
    
    updateStatus(`🔍 Loading ${year} precinct and county data...`);
    
    const contestParts = contest.split('_');
    let contestType = contestParts[0];

    // Map contestType to backend key
    if (contestType === 'us') {
        contestType = 'us_senate';
    } else if (contestType === 'attorney') {
        contestType = 'attorney_general';
    } else if (contestType === 'lt') {
        contestType = 'lt_governor';
    } else if (contestType === 'commissioner') {
        contestType = contestParts[0] + '_' + contestParts[1];
    } else if (contestType === 'state') {
        contestType = 'state_auditor';
    } else if (contestType === 'secretary') {
        contestType = 'secretary_of_state';
    } else if (contestType === 'treasurer') {
        contestType = 'treasurer';
    } else if (contestType === 'auditor') {
        contestType = 'state_auditor';
    } else if (contestType === 'superintendent') {
        contestType = 'superintendent_instruction';
    }

    console.log('Contest type:', contestType, 'from value:', contest);
    updateStatus(`🔍 Loading ${contestType} ${year}...`);
    
    console.log('Available years:', Object.keys(electionData.results_by_year || {}));
    if (electionData.results_by_year[year]) {
        console.log(`Available contests for ${year}:`, Object.keys(electionData.results_by_year[year]));
    }
    
    if (!electionData.results_by_year[year]) {
        updateStatus(`❌ No data for year ${year}`);
        return;
    }
    
    if (!electionData.results_by_year[year][contestType]) {
        updateStatus(`❌ No ${contestType} data for ${year}`);
        return;
    }
    
    const contestGroup = electionData.results_by_year[year][contestType];
    const contestKey = Object.keys(contestGroup)[0];
    const contestData = contestGroup[contestKey];
    
    if (!contestData.results) {
        updateStatus(`❌ No results found for ${contestKey}`);
        return;
    }
    
    const results = contestData.results;
    currentElectionResults = results;
    const precinctCount = Object.keys(results).length;
    updateStatus(`📊 Processing ${precinctCount} precincts for ${contestType} ${year}...`);
    
    updateStatewideResults(results, contestType, year);
    console.log(`Found ${precinctCount} precincts for ${contestType} ${year}`);
    
    if (currentMode === 'county') {
        applyCountyCategories(results, contestType, year);
    } else {
        applyPrecinctCategories(results, contestType, year);
    }
}

// TODO: Update data loading logic to use Georgia GeoJSON and election data files
// Example:
// const countyResponse = await fetch('./tl_2020_13_county.geojson');
// const counties = await countyResponse.json();
// map.addSource('counties', { type: 'geojson', data: counties });
// const precinctResponse = await fetch('./tl_2020_13_vtd20.geojson');
// const precincts = await precinctResponse.json();
// map.addSource('precincts', { type: 'geojson', data: precincts });
// const electionResponse = await fetch('./ga_statewide_precinct_comprehensive_2008_2024.json');
// electionData = await electionResponse.json();

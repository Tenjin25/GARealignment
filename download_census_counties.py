
import requests
import zipfile
import io
import os
import time
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_2008_vtd_zips(base_url, out_dir='data/2008_vtd'):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Fetching county folders from {base_url} ...")
    r = requests.get(base_url, verify=False)
    if r.status_code != 200:
        print(f"Failed to access directory: {base_url}")
        return
    soup = BeautifulSoup(r.text, 'html.parser')
    county_folders = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('/') and a['href'] != '../' and a['href'].startswith('13')]
    print(f"Found {len(county_folders)} county folders.")
    missing_vtd = []
    failed_downloads = []
    successful = []
    for folder in county_folders:
        folder_url = base_url + folder
        fips = folder.strip('/').split('_')[0]
        print(f"Checking {folder_url} ...")
        r2 = requests.get(folder_url, verify=False)
        if r2.status_code != 200:
            print(f"  Failed to access {folder_url}")
            missing_vtd.append(fips)
            continue
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        # List all .zip files for manual inspection
        all_zips = [a['href'] for a in soup2.find_all('a', href=True) if a['href'].endswith('.zip')]
        if all_zips:
            print(f"  All ZIP files in {folder_url}: {', '.join(all_zips)}")
        else:
            print(f"  No ZIP files found in {folder_url}")

        vtd_zips = [z for z in all_zips if 'vtd' in z.lower()]
        if not vtd_zips:
            print(f"  No VTD ZIP found for county FIPS {fips}")
            missing_vtd.append(fips)
            continue
        county_success = False
        for zipname in vtd_zips:
            url = folder_url + zipname
            print(f"  Downloading {url} ...")
            max_retries = 3
            for attempt in range(1, max_retries + 1):
                try:
                    resp = requests.get(url, verify=False)
                    if resp.status_code == 200:
                        try:
                            z = zipfile.ZipFile(io.BytesIO(resp.content))
                            z.extractall(out_dir)
                            print(f"    Extracted {zipname} to {out_dir}")
                            county_success = True
                            break  # Success, exit retry loop
                        except Exception as e:
                            print(f"    Error extracting {zipname}: {e}")
                            if attempt == max_retries:
                                failed_downloads.append(fips)
                    else:
                        print(f"    Failed to download: {url} (status {resp.status_code}), attempt {attempt}")
                        if attempt == max_retries:
                            failed_downloads.append(fips)
                    if attempt < max_retries:
                        time.sleep(2)
                except Exception as e:
                    print(f"    Exception during download: {e}, attempt {attempt}")
                    if attempt == max_retries:
                        failed_downloads.append(fips)
                    if attempt < max_retries:
                        time.sleep(2)
        if county_success:
            successful.append(fips)
        else:
            print(f"  No VTD ZIPs could be successfully downloaded for county FIPS {fips}")
            missing_vtd.append(fips)
    print("\nSummary:")
    print(f"  Successful downloads: {len(successful)} counties")
    if missing_vtd:
        print(f"  Counties with no VTD ZIP: {len(missing_vtd)}")
        print(f"    FIPS: {', '.join(missing_vtd)}")
    if failed_downloads:
        print(f"  Counties with failed downloads: {len(failed_downloads)}")
        print(f"    FIPS: {', '.join(failed_downloads)}")

if __name__ == '__main__':
    # Download all 2009 VTD shapefiles for Georgia counties
    base_url = 'https://www2.census.gov/geo/tiger/TIGER2009/13_GEORGIA/'
    download_2008_vtd_zips(base_url, out_dir='data/2009_vtd')
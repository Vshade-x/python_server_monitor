import requests
import pandas as pd
import os
import argparse
from requests.exceptions import RequestException
import sys # Needed to exit program gracefully

# ==========================================================
# 1. CONFIGURATION AND CONSTANTS
# ==========================================================

INPUT_FILE = "url_list.csv"
OUTPUT_FILE = "server_health_report.xlsx"
TIMEOUT_SECONDS = 10 

# List to store the final verification results
health_results = [] 

# ==========================================================
# 2. ARGUMENT PARSING
# ==========================================================

def parse_arguments():
    """Reads command line arguments for quick URL check."""
    parser = argparse.ArgumentParser(
        description="A Python tool to monitor the health status of a list of URLs or a single URL.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Argument for single URL check (optional)
    parser.add_argument(
        '--url', 
        '-u',
        type=str,
        default=None,
        help="Check a single URL immediately without processing the list file."
    )
    return parser.parse_args()

# ==========================================================
# 3. CORE LOGIC: CHECK STATUS FOR ONE URL
# ==========================================================

def check_single_url(url):
    """Performs a single HTTP HEAD request and returns the result dictionary."""
    # Skip if the URL field is empty
    if pd.isna(url) or url == '':
        return None
        
    # Ensure URL has a scheme for requests (http:// or https://)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        # Use requests.head() for a faster, lighter request
        response = requests.head(url, timeout=TIMEOUT_SECONDS, allow_redirects=True)
        
        status_code = response.status_code
        
        if status_code < 400:
            health_status = "ONLINE"
        elif status_code >= 400 and status_code < 500:
            health_status = "CLIENT ERROR (e.g., 404 Not Found)"
        else:
            health_status = "SERVER ERROR (e.g., 500 Internal Error)"
        
    except requests.exceptions.RequestException as e:
        # Handle all connection errors (DNS failure, timeout, no internet, etc.)
        status_code = 'N/A'
        health_status = f"OFFLINE/CONNECTION FAILED: {e.__class__.__name__}"
    
    print(f"Checked: {url} -> {health_status} (Code: {status_code})")
    
    return {
        'URL Checked': url,
        'HTTP Status Code': status_code,
        'Health Status': health_status
    }

# ==========================================================
# 4. EXPORT FUNCTION
# ==========================================================

def export_results(results_list):
    """Exports the list of health check results to a structured Excel file."""
    df = pd.DataFrame(results_list)
    
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print("\n==============================================")
        print(f"✅ SUCCESS! Health Report saved to: {OUTPUT_FILE}")
        print(f"Total entries checked: {len(df)}")
        print("==============================================")
    except Exception as e:
        print(f"❌ EXPORT ERROR: Could not write to Excel file: {e}")

# ==========================================================
# 5. MAIN EXECUTION FLOW
# ==========================================================

def main_execution(args):
    """Handles the main logic, prioritizing the command line argument."""
    
    # --- FLOW A: Single URL Check (Prioritized) ---
    if args.url:
        print(f"Starting INSTANT health check for single URL...")
        result = check_single_url(args.url)
        
        if result:
            export_results([result])
        sys.exit(0)

    # --- FLOW B: Bulk File Check ---
    print(f"Starting BULK health check on URLs from: {INPUT_FILE}")
    
    try:
        # Load the CSV file containing the URLs
        df_urls = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"❌ ERROR: The file '{INPUT_FILE}' was not found. Cannot perform bulk check.")
        return

    # Iteration and Request Logic
    for index, row in df_urls.iterrows():
        url = row['URL']
        result = check_single_url(url)
        if result:
            health_results.append(result)

    # Final Export
    if health_results:
        export_results(health_results)
    else:
        print("⚠️ WARNING: No valid URLs were processed from the file.")


if __name__ == "__main__":
    args = parse_arguments()
    main_execution(args)
import gspread
import logging
import os
import pandas as pd
import requests
import subprocess
from oauth2client.service_account import ServiceAccountCredentials

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_existing_data(file_path):
    """Reads existing data from a CSV file to compare with newly fetched data."""
    if os.path.exists(file_path):
        logging.info("Existing data file found. Reading data...")
        return pd.read_csv(file_path)
    else:
        logging.info("No existing data file found.")
        return pd.DataFrame()  # Return an empty DataFrame if file does not exist

def download_sheet(sheet_id, range_name):
    """Downloads data from Google Sheets and returns a DataFrame."""
    try:
        # Define the scope
        scope = ['https://www.googleapis.com/auth/spreadsheets']

        # Add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name('omoku-analysis-cred_key.json', scope)

        # Authorize the clientsheet 
        client = gspread.authorize(creds)

        # Get the instance of the Spreadsheet
        sheet = client.open_by_key(sheet_id)

        # Get the sheet by name
        worksheet = sheet.get_worksheet(0)

        # Get all records of the data
        data = worksheet.get_all_records()

        # Convert to DataFrame
        df = pd.DataFrame(data)
        return df
    except gspread.exceptions.APIError as e:
        logging.error(f"API error occurred: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise

def save_to_csv(df, file_path):
    if df.empty:
        logging.error("No data to save: DataFrame is empty.")
        raise ValueError("Empty DataFrame")
    try:
        df.to_csv(file_path, index=False)
        logging.info(f"Data saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")
        raise

def git_commit_push():
    """Sets git configurations, commits, and pushes updated CSV file to GitHub."""
    try:
        subprocess.run(['git', 'config', '--global', 'user.name', 'github-actions'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'github-actions@github.com'], check=True)
        subprocess.run(['git', 'add', 'omoku_data.csv'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Update dataset'], check=True)
        subprocess.run(['git', 'push'], check=True)
        logging.info(f"Data updated successfully.")
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in str(e.stderr):
            logging.info("No changes to commit.")
        else:
            logging.error(f"Failed to commit or push changes: {e}")
            raise

if __name__ == "__main__":
    try:
        SHEET_ID = '1dVa6SGm1j-z20NUDUlWSJgQffXzvJZ_a33wT_O5EOUk'
        RANGE_NAME = 'data'
        FILE_PATH = 'omoku_data.csv'

        new_data = download_sheet(SHEET_ID, RANGE_NAME)
        existing_data = read_existing_data(FILE_PATH)

        if not new_data.empty and new_data.equals(existing_data):
            logging.info("No new data to update.")
            exit(0)
    
        save_to_csv(new_data, FILE_PATH)
        git_commit_push()
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")
        raise

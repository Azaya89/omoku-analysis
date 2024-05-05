import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import subprocess

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
        print(f"API error occurred: {e}")
        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise SystemExit(e)

def save_to_csv(df, file_path):
    if df.empty:
        raise SystemExit("No data to save: DataFrame is empty.")
    try:
        df.to_csv(file_path, index=False)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Failed to save data: {e}")
        raise SystemExit(e)

def git_commit_push():
    """Sets git configurations, commits, and pushes updated CSV file to GitHub."""
    try:
        subprocess.run(['git', 'config', '--global', 'user.name', 'github-actions'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'github-actions@github.com'], check=True)
        subprocess.run(['git', 'add', 'omoku_data.csv'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to commit or push changes: {e}")
        if "nothing to commit" in str(e.stderr):
            print("No changes to commit.")
        else:
            raise SystemExit(e)
        
    try:
        subprocess.run(['git', 'commit', '-m', 'Update dataset'], check=True)
        subprocess.run(['git', 'push'], check=True)
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in str(e):
            print("No changes to commit.")
        else:
            print(f'Error in Git operation: {e}')

if __name__ == "__main__":
    try:   
        SHEET_ID = '1dVa6SGm1j-z20NUDUlWSJgQffXzvJZ_a33wT_O5EOUk'
        RANGE_NAME = 'data'
        FILE_PATH = 'omoku_data.csv'

        df = download_sheet(SHEET_ID, RANGE_NAME)
        save_to_csv(df, FILE_PATH)
        git_commit_push()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise SystemExit(e)

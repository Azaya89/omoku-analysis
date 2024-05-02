import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess

def download_sheet(sheet_id, range_name):
    """Downloads data from Google Sheets and returns a DataFrame."""
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

def save_to_csv(df, file_path):
    """Saves DataFrame to CSV."""
    df.to_csv(file_path, index=False)


def git_commit_push():
    """Commits and pushes updated CSV file to GitHub."""
    subprocess.run(['git', 'add', 'omoku_data.csv'], check=True)
    try:
        subprocess.run(['git', 'commit', '-m', 'Update dataset'], check=True)
        subprocess.run(['git', 'push'], check=True)
    except subprocess.CalledProcessError as e:
        if "nothing to commit" in str(e):
            print("No changes to commit.")
        else:
            print(f'Error in Git operation: {e}')

if __name__ == "__main__":
    SHEET_ID = '1dVa6SGm1j-z20NUDUlWSJgQffXzvJZ_a33wT_O5EOUk'
    RANGE_NAME = 'data'
    FILE_PATH = 'omoku_data.csv'

    df = download_sheet(SHEET_ID, RANGE_NAME)
    save_to_csv(df, FILE_PATH)
    git_commit_push()

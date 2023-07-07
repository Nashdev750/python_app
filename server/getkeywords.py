import gspread
from google.oauth2.service_account import Credentials

def read_google_sheet_column():
    sheet_id = '15wyOQXktRxDa4fR6UV461_aDrMpx8VWq7f83MT11oM4'

    sheet_name = 'Sheet1'
    column = 1
    # Set up the credentials
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_service_account_file('credentials.json', scopes=scopes)

    # Authorize the client
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(sheet_name)

    # Read the values from the specified column
    values = worksheet.col_values(column)

    return values


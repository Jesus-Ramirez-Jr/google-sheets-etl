import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import os

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

CREDENTIALS_FILE = 'first-etl-496805-8beb6f61dbda.json'
SPREADSHEET_NAME = 'aaac'


def authenticate():
    try:
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        print("Authentication Successful")
        return client
    except FileNotFoundError:
        print(f"Error: Credentials File '{CREDENTIALS_FILE}' not found")
        raise
    except Exception as e:
        print(f"Authentication failed: {e}")
        raise


def extract(client):
    try:
        sheet = client.open('aaac').sheet1
        data = sheet.get_all_records()
        print("Extraction Successful")
        return data
    except gspread.SpreadsheetNotFound:
        print(f"Error: {SPREADSHEET_NAME} not found")
        raise
    except gspread.exceptions.APIError:
        print(f"Error: security rights needed")
        raise
    except Exception as e:
        print(f"Error: Extract Error {e}")
        raise


def transform(data):
    try:
        df = pd.DataFrame(data)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        print("Transform Successful")
        return df
    except TypeError:
        print(f"Error: Transform Error: {e}")
        raise
    except Exception as e:
        print(f"Transform Failed: {e}")
        raise


def load(df, table_name='assets'):
    try:
        engine = create_engine(
            f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@localhost/{os.environ.get('DB_NAME')}")
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Successfully loaded {len(df)} rows into {table_name}")
    except OperationalError:
        print(f"Error: Access Denied, Unable to connect to localhost")
        raise
    except Exception as e:
        print(f"Loading failed: {e}")
        raise


def main():
    client = authenticate()
    data = extract(client)
    df = transform(data)
    load(df)


if __name__ == '__main__':
    main()

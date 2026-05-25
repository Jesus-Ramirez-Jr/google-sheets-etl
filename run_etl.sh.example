#!/bin/bash
export DB_USER='your_db_user'
export DB_PASSWORD='your_db_password'
export DB_NAME='your_db_name'
export GOOGLE_CREDENTIALS_FILE='your_credentials.json'

cd /Users/jr/Projects/google_sheets_etl
source venv/bin/activate
python etl.py >> /Users/jr/Projects/google_sheets_etl/etl.log 2>&1

# Google Sheets → MySQL ETL Pipeline

A lightweight Python script that extracts data from a Google Sheet, transforms it with pandas, and loads it into a MySQL database. Built to understand the ETL process that tools like Airbyte automate, and to serve as a manual fallback when those tools fail.

---

## Why This Exists

Airbyte handles our Google Sheets ingestion in production, but it's a black box. This project was built to:

- Understand what Airbyte is actually doing under the hood (authenticate → extract → transform → load)
- Have a working manual backup if Airbyte goes down

---

## How It Works

The script follows a standard ETL flow:

1. **Authenticate** — Connects to Google Sheets using a service account credentials file (JSON)
2. **Extract** — Pulls data from the target sheet using `gspread`
3. **Transform** — Cleans and structures the data using `pandas`
4. **Load** — Writes the result to a local MySQL database via `SQLAlchemy`

Error handling is implemented at each stage so failures are easy to isolate and debug.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core scripting language |
| gspread | Google Sheets API client |
| pandas | Data transformation |
| SQLAlchemy | Database connection and ORM |
| MySQL | Target database |
| Google Sheets | Data source |

---

## Setup & Usage

### Prerequisites

- Python 3.x
- A Google Cloud service account with Sheets API access
- A MySQL instance running locally (or update the connection string for remote)

### Steps

```bash
# 1. Clone the repo
git clone <repo-url>
cd <repo-folder>

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Google credentials
# Download the service account JSON from Google Cloud Console
# Save it to the project root (do not commit this file)

# 5. Set environment variables
export DB_USER=your_mysql_username
export DB_PASSWORD=your_mysql_password
export DB_NAME=your_db_name

# 6. Run the script
python etl.py
```

> **Note:** Never hardcode credentials. DB username and password are passed via environment variables. The Google credentials JSON should be listed in `.gitignore`.

---

## Key Concepts Covered

- **Google Cloud authentication** — How to create a service account, download credentials as JSON, and grant it access to a specific sheet
- **gspread permissions** — What access level the service account needs and how it's configured in the script
- **Environment variables** — Why we use them instead of hardcoding secrets, and how to set them locally
- **ETL flow** — Hands-on understanding of authenticate → extract → transform → load as discrete, debuggable steps
- **Dependency management** — Setting up a virtual environment and `requirements.txt`

---

## What I learn
- **Sync modes** — understanding the difference between full refresh and incremental and how if_exists='replace' mirrors Airbyte's full refresh overwrite behavior
- **Least privilege principle** — why scopes are set to readonly and why that matters
- **Reading tracebacks** — how to isolate the actual error from the noise

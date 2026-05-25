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

# 6. Run the script
python etl.py
```

> **Note:** Never hardcode credentials. DB username and password are passed via environment variables. The Google credentials JSON should be listed in `.gitignore`.

---

## Automated Scheduling (Cron)

The ETL runs automatically every **Monday at 9:00 AM** via cron.

### How it works

- `run_etl.sh.example` — Template file committed to the repo. Contains placeholder credentials. Copy this file, rename it to `run_etl.sh`, and fill in your actual values.
- `run_etl.sh` — Your local copy with real credentials. **Never commit this file.** Make sure it's in `.gitignore`.

`run_etl.sh` exports environment variables and then calls `etl.py`:

```bash
export DB_USER=your_actual_username
export DB_PASSWORD=your_actual_password
export DB_NAME=your_actual_db_name
python /Users/jr/Projects/google_sheets_etl/etl.py
```

### Crontab entry

```
0 9 * * 1 /Users/jr/Projects/google_sheets_etl/run_etl.sh
```

| Field | Value | Meaning |
|---|---|---|
| 0 | Minute | At :00 |
| 9 | Hour | 9 AM |
| * | Day of month | Any |
| * | Month | Any |
| 1 | Day of week | Monday only |

### To install or edit the cron job

```bash
crontab -e        # Open cron editor
crontab -l        # List current cron jobs
```

---

## Key Concepts Covered

- **Google Cloud authentication** — How to create a service account, download credentials as JSON, and grant it access to a specific sheet
- **gspread permissions** — What access level the service account needs and how it's configured in the script
- **Environment variables** — Why we use them instead of hardcoding secrets, and how to set them locally
- **ETL flow** — Hands-on understanding of authenticate → extract → transform → load as discrete, debuggable steps
- **Dependency management** — Setting up a virtual environment and `requirements.txt`
- **Cron scheduling** — How to automate script execution on a recurring schedule using crontab, and how to read cron syntax
- **Credential templating** — Using a dummy shell script (`run2_etl.sh`) as a safe, committable template while keeping the real credentials file (`run_etl.sh`) out of version control

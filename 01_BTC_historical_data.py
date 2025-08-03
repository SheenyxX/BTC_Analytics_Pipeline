import yfinance as yf
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account # Import for explicit credential loading
import os

# --- BigQuery Configuration ---
# Your Google Cloud Project ID
PROJECT_ID = "cr-btc-investment"
# Your BigQuery Dataset ID (e.g., 'btc_investments')
DATASET_ID = "btc_investments" # You will need to create this dataset in BigQuery if you haven't already
# Table ID for historical BTC prices
TABLE_ID = "historical_btc_prices"

# --- Service Account Key Configuration ---
# IMPORTANT: It is generally recommended to use the GOOGLE_APPLICATION_CREDENTIALS
# environment variable or default credentials when running on GCP (e.g., Cloud Functions).
# Hardcoding the path here is less secure for production but can be convenient for local testing.
# If you use this, ensure the JSON key file is stored securely and not committed to public repositories.

# Option 1 (Recommended for local dev): Set GOOGLE_APPLICATION_CREDENTIALS environment variable.
#   On Windows Command Prompt: set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
#   On Windows PowerShell: $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
#   On macOS/Linux: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
# The BigQuery client will automatically pick up this environment variable.

# Option 2 (Direct path in code - use with caution for production):
# Uncomment the line below and replace with the actual path to your JSON key file.
SERVICE_ACCOUNT_KEY_PATH = r"C:\Users\drewr\OneDrive\Escritorio\Google Cloud Training\CR Investment BTC\cr-btc-investment-86a4c114e04e.json"
# If you use this, ensure the environment variable GOOGLE_APPLICATION_CREDENTIALS is NOT set,
# or this explicit path will take precedence.

# --- Data Fetching Configuration ---
TICKER_SYMBOL = "BTC-USD"
# Start date for historical data. Fetch from your earliest investment date.
# We'll fetch from a slightly earlier date to ensure full historical context.
START_DATE = "2024-08-01" # Fetch from August 1, 2024 to be safe
END_DATE = datetime.now().strftime("%Y-%m-%d") # Today's date

# --- Main Script ---
def fetch_and_upload_btc_data():
    print(f"Starting data fetch and upload for {TICKER_SYMBOL}...")
    print(f"Fetching data from {START_DATE} to {END_DATE}...")

    try:
        # 1. Fetch historical data using yfinance
        # Include 'Volume' in the downloaded data
        btc_data = yf.download(TICKER_SYMBOL, start=START_DATE, end=END_DATE, interval="1d")

        if btc_data.empty:
            print("No data fetched. Please check the ticker symbol and date range.")
            return

        # --- FIX: Correctly handle MultiIndex columns from yfinance ---
        # yfinance can return a MultiIndex. If so, level 0 is the data type ('Open', 'Close')
        # and level 1 is the ticker ('BTC-USD'). We need to drop the ticker level (level 1).
        if isinstance(btc_data.columns, pd.MultiIndex):
            btc_data.columns = btc_data.columns.droplevel(1)
        # --- END FIX ---

        # Reset index to make 'Date' a regular column
        btc_data_reset = btc_data.reset_index()

        # Debugging: Print columns to see what's actually there after flattening and reset
        print("Columns after flattening and reset_index():", btc_data_reset.columns.tolist())

        # Add a check for required columns to make the script more robust
        required_cols = ['Date', 'Close', 'Volume']
        if not all(col in btc_data_reset.columns for col in required_cols):
            print(f"\nError: DataFrame is missing one or more required columns: {required_cols}")
            print(f"Actual columns found: {btc_data_reset.columns.tolist()}")
            print("This can happen if the yfinance API output has changed. Please check the column names printed above.")
            return

        # Select 'Date', 'Close' price, and 'Volume' columns
        # Use .copy() to prevent a pandas SettingWithCopyWarning later
        historical_prices_df = btc_data_reset[required_cols].copy()

        # Rename DataFrame columns to match the BigQuery schema
        historical_prices_df = historical_prices_df.rename(columns={
            'Close': 'BTC_Price_USD',
            'Volume': 'Volume_USD'
        })

        # Ensure 'Date' column is datetime.date objects for pyarrow/BigQuery compatibility
        historical_prices_df['Date'] = pd.to_datetime(historical_prices_df['Date']).dt.date
        
        # --- EDIT: Sort data by date before uploading ---
        historical_prices_df.sort_values(by='Date', inplace=True)
        # --- END EDIT ---

        # Cast numeric columns to INTEGER to remove decimals
        historical_prices_df['BTC_Price_USD'] = historical_prices_df['BTC_Price_USD'].astype(float).astype(int)
        historical_prices_df['Volume_USD'] = historical_prices_df['Volume_USD'].astype(float).astype(int)

        print(f"\nSuccessfully fetched {len(historical_prices_df)} rows of historical BTC data.")
        print("Columns being sent to BigQuery:", historical_prices_df.columns.tolist())
        print("\nFirst 5 rows of data to be uploaded:")
        print(historical_prices_df.tail())

        # 2. Initialize BigQuery client
        if SERVICE_ACCOUNT_KEY_PATH and os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
            credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_KEY_PATH)
            client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
            print(f"\nUsing service account key from: {SERVICE_ACCOUNT_KEY_PATH}")
        else:
            client = bigquery.Client(project=PROJECT_ID)
            print("\nUsing GOOGLE_APPLICATION_CREDENTIALS environment variable or default credentials.")

        table_ref = client.dataset(DATASET_ID).table(TABLE_ID)

        # 3. Define BigQuery table schema
        schema = [
            bigquery.SchemaField("Date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("BTC_Price_USD", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("Volume_USD", "INTEGER", mode="REQUIRED"),
        ]

        # 4. Configure the load job
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        # 5. Upload data to BigQuery
        print(f"\nUploading data to BigQuery table: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}...")
        job = client.load_table_from_dataframe(
            historical_prices_df, table_ref, job_config=job_config
        )

        job.result() # Waits for the job to complete
        print(f"Successfully loaded {job.output_rows} rows into BigQuery table '{TABLE_ID}'.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("\nPlease ensure:")
        print("1. You have an active internet connection.")
        print("2. 'yfinance', 'pandas', 'google-cloud-bigquery', and 'pyarrow' libraries are installed.")
        print("   You can install them using: pip install yfinance pandas google-cloud-bigquery pyarrow")
        print(f"3. Your Google Cloud Project ID ('{PROJECT_ID}'), Dataset ID ('{DATASET_ID}'), and Table ID ('{TABLE_ID}') are correct.")
        print("4. Your service account credentials are correctly configured.")
        print("   Also, ensure the service account has the necessary BigQuery permissions (e.g., BigQuery Data Editor).")

# Call the function to run the script
if __name__ == "__main__":
    fetch_and_upload_btc_data()

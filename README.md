# Bitcoin Portfolio Tracker & Analytics

[](https://www.python.org/)
[](https://www.google.com/sheets/about/)
[](https://powerbi.microsoft.com/)

## Overview

The Bitcoin Portfolio Tracker & Analytics project is a data-driven solution designed to provide comprehensive insights into your Bitcoin investment performance. This project automates the collection, processing, and visualization of investment and market data, delivering key metrics through an interactive Power BI dashboard. It showcases robust data integration, custom DAX calculations, and effective business intelligence reporting.

## Key Features

The Power BI dashboards provide the following key insights:

**1. Investment Overview:**

  * **Current Live BTC Price:** Real-time Bitcoin price.
  * **Total Current Portfolio Value (USD):** Your portfolio's current market value.
  * **Total Amount Invested (USD):** The total capital invested.
  * **Total Unrealized PnL (USD):** Overall profit or loss on your investment.
  * **Overall ROI Percent:** Percentage return on your total investment.

**2. Individual Purchase Analysis:**

  * **Current Value (USD):** The current value of each specific BTC purchase.
  * **Unrealized PnL (USD):** Profit or loss for individual purchases.
  * **Calculated ROI Percent:** ROI for each individual BTC purchase.

**3. Data Integration:**

  * Direct connection to **yfinance** for historical BTC prices.
  * Integration with **Google Sheets** for investment purchase records.

**4. Dashboard Functionality:**

  * Interactive dashboard with a summary view for overall portfolio metrics and a detailed purchase history.
  * Automated daily refresh ensures all metrics are based on the latest available end-of-day data.
  * Designed for a responsive viewing experience across various devices.

*(Optional: Add your dashboard screenshots here)*

## Technologies Used

  * **Python:** For data extraction, transformation, and loading (ETL).
      * `yfinance`: To fetch historical cryptocurrency price data.
      * `pandas`: For data manipulation and creating DataFrames.
      * `gspread`: To interact with Google Sheets for investment records.
      * `google-auth-oauthlib`, `google.oauth2.credentials`: For authenticating and interacting with Google services (for `gspread`).
      * `datetime`: For handling date and time information.
  * **Google Cloud Platform (GCP):**
      * **Google Sheets:** Utilized for storing individual investment purchase records.
  * **Microsoft Power BI:** For data visualization and creating interactive dashboards and reports with custom DAX measures.

## Data Pipeline Process

The project implements an automated data pipeline:

1.  **Data Extraction:**
      * A Python script fetches historical BTC price data using **yfinance**.
      * Investment purchase records are retrieved from a designated **Google Sheet** using the `gspread` library.
2.  **Data Transformation:**
      * Raw data from yfinance and Google Sheets is parsed and transformed into structured formats using Python and Pandas, extracting relevant metrics.
      * Data cleaning and formatting are performed to ensure consistency and suitability for analysis.
3.  **Data Loading:**
      * The processed data (e.g., as intermediate CSV files or directly via Python/Power Query connectors) is made available for consumption by Power BI.
4.  **Data Visualization:**
      * Data from the prepared sources (yfinance output, Google Sheet) is connected to Microsoft Power BI.
      * Custom **DAX measures** are defined within Power BI to calculate key investment performance indicators such as `Unrealized_PnL_USD`, `Total_Current_Portfolio_Value_USD`, `Overall_ROI_Percent`, `Current_Value_USD`, and `Calculated_ROI_Percent`.
      * Interactive dashboards are created to visualize these metrics, offering both an overall portfolio summary and detailed insights into individual purchases.

## Setup and Usage

To set up and use this project, you will need:

1.  **Google Account:** Required to access Google Sheets.
2.  **Google Sheets API Access:** You'll need to enable the Google Sheets API in your Google Cloud Project and set up appropriate credentials (e.g., a service account or OAuth 2.0 desktop application) for `gspread` to access your sheet.
3.  **Python Environment:** Ensure you have Python 3.x installed along with the required libraries. You can install them via pip:
    ```bash
    pip install yfinance pandas gspread google-auth-oauthlib google-oauth2-credentials
    ```
4.  **Power BI Desktop:** Microsoft Power BI Desktop is required to connect to your prepared data sources (output from Python scripts, Google Sheet) and view the dashboards.
5.  **Google Sheet for Investments:** Set up a Google Sheet with your investment purchase records. Ensure the sheet's sharing settings or your Google Cloud credentials allow access by your Python script.

## Further Development

Potential future enhancements could include:

  * Expanding the analysis to include other cryptocurrencies in the investment portfolio.
  * Adding more advanced forecasting or anomaly detection capabilities.
  * Integrating data from additional cryptocurrency exchanges or data providers (if moving beyond `yfinance`).
  * Developing a more dynamic and user-configurable dashboard in Power BI.

-----

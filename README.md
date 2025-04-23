# BTC Analytics Pipeline

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![BigQuery](https://img.shields.io/badge/BigQuery-GoogleCloud-blue.svg)](https://cloud.google.com/bigquery)
[![Power BI](https://img.shields.io/badge/Power_BI-Microsoft-blue.svg)](https://powerbi.microsoft.com/)

## Overview

The BTC Analytics Pipeline is a data-driven project designed to provide comprehensive insights into Bitcoin (BTC) investment performance and broader cryptocurrency market dynamics. This project automates the collection, processing, and visualization of cryptocurrency data to deliver key metrics and reports through an interactive Power BI dashboard. Initially conceived to track the performance of a specific BTC investment made at $63,000 on October 13, 2024, the pipeline has evolved to offer a broader understanding of the cryptocurrency market.

This project demonstrates the application of data engineering and business intelligence skills to a real-world financial tracking scenario.

## Key Features

The Power BI dashboards provide the following key insights:

**1. BTC Price & Metrics:**

* **Current BTC Price:** Real-time USD price of Bitcoin.
* **Price Change (%):** Percentage change in BTC price over various timeframes (24h, 7d, 30d, 60d, 90d).
* **Volume Metrics:**
    * **24h Volume:** Total trading volume of BTC in the last 24 hours.
    * **24h Volume Change (%):** Percentage change in BTC trading volume in the last 24 hours.
* **Market Capitalization:** Current market cap of Bitcoin.
* **BTC Dominance (%):** Bitcoin's share of the total cryptocurrency market capitalization.

![BTC Price & Metrics Dashboard Screenshot](https://github.com/SheenyxX/BTC_Analytics_Pipeline/blob/main/BTC%20D%201.png)

**2. BTC Investment Report:**

* **BTC Price Over Time:** An interactive chart visualizing BTC price history from the initial investment date (October 13, 2024) to the present. The initial purchase price of $63,000 is clearly marked.
* **Monthly Volume:** Chart displaying the monthly trading volume of BTC.
* **Overall Price Change (%):** Percentage change in BTC price from the initial purchase date to the current date.
* **Investment Performance:**
    * **Cost of Investment:** The initial amount invested in BTC.
    * **Current Investment Value:** The current market value of the invested BTC.
    * **Profit:** The difference between the current investment value and the cost of investment.
    * **Return on Investment (ROI):** The percentage return on the initial investment.

![BTC Investment Report Dashboard Screenshot](https://github.com/SheenyxX/BTC_Analytics_Pipeline/blob/main/BTC%20D%202.png)

**3. Cryptocurrency Market 24h Volume:**

* **Top Volume Cryptocurrencies:** A bar chart highlighting the 24-hour trading volume of major cryptocurrencies (e.g., USDT, BTC, ETH, USDC).
* **Other Cryptocurrencies Volume:** A separate bar chart showing the 24-hour trading volume of the remaining cryptocurrencies in the dataset, providing a broader market context.

![Cryptocurrency Market 24h Volume Dashboard Screenshot](https://github.com/SheenyxX/BTC_Analytics_Pipeline/blob/main/BTC%20D%203.png)

**4. Cryptocurrency Market Cap Visualization:**

* **Market Cap Squares:** A visual representation of the cryptocurrency market capitalization, where the size of each square corresponds to the market cap of a specific cryptocurrency. This provides an intuitive understanding of market dominance, with Bitcoin's dominance being visually prominent.

![Cryptocurrency Market Cap Visualization Dashboard Screenshot](https://github.com/SheenyxX/BTC_Analytics_Pipeline/blob/main/BTC%20D%204.png)

## Technologies Used

* **Python:** For data extraction, transformation, and loading (ETL).
    * **`requests`:** To interact with the CoinMarketCap API.
    * **`json`:** To handle JSON responses from the API.
    * **`pandas`:** For data manipulation and creating DataFrames.
    * **`ccxt`:** To fetch historical BTC price data from the Binance exchange.
    * **`google-cloud-bigquery`:** To interact with Google BigQuery.
    * **`google-oauth2`:** For authenticating with Google Cloud services.
    * **`datetime`:** For handling date and time information.
* **Google Cloud Platform (GCP):**
    * **Google BigQuery:** As the scalable and serverless data warehouse for storing and querying cryptocurrency data.
* **Microsoft Power BI:** For data visualization and creating interactive dashboards and reports.

## Data Pipeline Process

The project implements a weekly automated data pipeline:

1.  **Data Extraction:**
    * The Python script fetches the latest cryptocurrency market data from the CoinMarketCap API.
    * Historical daily BTC/USDT price data is retrieved from the Binance exchange using the CCXT library, starting from August 19, 2024, to ensure sufficient historical context for the investment report.
2.  **Data Transformation:**
    * The raw JSON data from CoinMarketCap is parsed and transformed into a structured Pandas DataFrame, extracting relevant metrics like price, volume, and market capitalization.
    * The OHLCV (Open, High, Low, Close, Volume) data from CCXT is converted into a Pandas DataFrame with appropriate column names and a datetime index.
    * Data cleaning and formatting are performed to ensure consistency and suitability for loading into BigQuery.
3.  **Data Loading:**
    * The processed DataFrames are loaded into Google BigQuery tables within the `Crypto_Dataset_Bucket` dataset. The `WRITE_TRUNCATE` disposition is used to replace the existing data with the latest weekly update, ensuring the dashboards reflect the most current information.
4.  **Data Visualization:**
    * The data stored in BigQuery is connected to Microsoft Power BI.
    * Power BI is used to create the interactive dashboards showcasing the BTC Price & Metrics, BTC Investment Report, Cryptocurrency Market 24h Volume, and Cryptocurrency Market Cap Visualization.

## Setup and Usage (Conceptual - Adapt as needed for your sharing intentions)

While this project is currently designed for automated weekly updates, the following outlines the conceptual setup:

1.  **Google Cloud Account:** A Google Cloud Platform account is required to utilize BigQuery.
2.  **Service Account:** A Google Cloud service account with the necessary permissions to write data to BigQuery needs to be created. The service account key file (`key-btc-investment-1.json` in the provided code) should be securely managed.
3.  **CoinMarketCap API Key:** A valid API key from CoinMarketCap is required to access their data.
4.  **Python Environment:** Ensure you have Python 3.x installed along with the necessary libraries (`requests`, `pandas`, `ccxt`, `google-cloud-bigquery`, `google-auth`). You can install the requirements using `pip install requests pandas ccxt google-cloud-bigquery google-auth`.
5.  **Power BI Desktop:** Microsoft Power BI Desktop is required to connect to the BigQuery data source and view the dashboards.

**(Note:** If you are not intending for others to run this exact pipeline, you can adjust this section to describe the conceptual process or omit specific setup instructions.)

## Further Development (Optional)

Potential future enhancements could include:

* Implementing more advanced technical indicators in the Power BI dashboards.
* Expanding the analysis to include other cryptocurrencies in the investment portfolio.
* Adding anomaly detection or forecasting capabilities.
* Integrating data from additional cryptocurrency exchanges or data providers.
* Developing a more dynamic and user-configurable dashboard in Power BI.



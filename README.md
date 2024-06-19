# Cryptocurrency Portfolio Analyzer

## Overview
The Cryptocurrency Portfolio Analyzer is a Streamlit application designed to help users track and compare the performance of multiple cryptocurrency portfolios over a specified period. The app allows users to simulate periodic investments in various cryptocurrencies and visualize the growth of their portfolios.

## Features
- Add and compare multiple portfolios
- Select cryptocurrencies for each portfolio
- Choose investment period (day, week, month, year)
- Define the investment amount for each period
- Visualize portfolio performance over time
- Calculate the final value and profit percentage for each portfolio

## Installation
To run this application, you need to have Python and Streamlit installed on your system.

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/crypto-portfolio-analyzer.git
    cd crypto-portfolio-analyzer
    ```

2. **Install required packages**
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Prepare the data file**
   - The application expects a CSV file named `history_prices.csv` in the root directory.
   - The CSV file should contain the following columns:
     - `Date`: The date of the price data (in YYYY-MM-DD format)
     - `Coin`: The name of the cryptocurrency
     - `Close`: The closing price of the cryptocurrency on the given date

2. **Run the application**
    ```bash
    streamlit run app.py
    ```

3. **Interact with the Streamlit interface**
   - Use the sidebar to add portfolios, select cryptocurrencies, and set investment parameters.
   - Click the "Analyze" button to visualize the performance of your portfolios.

## Example
Here's a sample structure of the `history_prices.csv` file:
```csv
Date,Coin,Close
2023-01-01,BTC,30000
2023-01-01,ETH,2000
2023-02-01,BTC,32000
2023-02-01,ETH,2100


## Code Explanation
Main Components
Loading Data: The app loads historical cryptocurrency prices from history_prices.csv.
User Inputs: Users can add portfolios, select cryptocurrencies, and define investment parameters via the sidebar.
Portfolio Update Function: Updates the portfolio by adding the quantities of selected cryptocurrencies based on the investment amount.
Portfolio Value Calculation: Calculates the total value of the portfolio for each date.
Visualization: Plots the performance of each portfolio and compares it with a no-investment scenario.
Final Value and Profit Calculation: Displays the final value, total profit, and profit percentage for each portfolio.
Key Functions
update_portfolio(portfolio, coins, date, data, investment): Updates the portfolio with the selected cryptocurrencies.
calculate_portfolio_value(portfolio, date, data): Calculates the value of the portfolio on a given date.
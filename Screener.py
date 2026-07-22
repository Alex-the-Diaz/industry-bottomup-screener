import yfinance as yf  # Library that pulls live financial data from Yahoo Finance
import pandas as pd  # Library that organizes data into clean tables

# Ask the user to input tickers
print("\n--- Fragmented Industry Roll-Up Screener ---")
print("Enter stock tickers separated by commas (e.g. WERN, HTLD, MRTN):")
user_input = input("> ")  # Waits for the user to type something and stores it

# Clean up the input — removes extra spaces, makes everything uppercase
tickers = [t.strip().upper() for t in user_input.split(",")]

print(f"\nFetching data for: {tickers}\n")  # Confirms which tickers were entered

results = []  # Empty list that we'll fill with each company's data

for ticker in tickers:  # Loop through each ticker one at a time
    stock = yf.Ticker(ticker)  # Tell yfinance which company to look up
    info = stock.info  # Pull all available financial data for that company
    
    results.append({  # Add this company's key metrics to the results list
        "Company": info.get("longName", ticker),  # Full company name
        "Ticker": ticker,  # Stock ticker symbol
        "Market Cap ($M)": round(info.get("marketCap", 0) / 1_000_000, 1),  # Total company value in millions
        "Revenue ($M)": round(info.get("totalRevenue", 0) / 1_000_000, 1),  # Annual revenue in millions
        "EBITDA ($M)": round(info.get("ebitda", 0) / 1_000_000, 1),  # Earnings before interest, taxes, depreciation
        "Profit Margin (%)": round(info.get("profitMargins", 0) * 100, 2),  # Net profit as a percentage of revenue
        "EV/EBITDA": round(info.get("enterpriseToEbitda", 0), 2),  # Valuation multiple — lower = cheaper acquisition
    })

df = pd.DataFrame(results)  # Convert the results list into a structured table
df = df.sort_values("Market Cap ($M)")  # Sort smallest to largest — smallest are best roll-up targets

print("\n--- Results: Ranked by Market Cap (Smallest = Best Roll-Up Targets) ---\n")
print(df.to_string(index=False))  # Print the full table without row numbers
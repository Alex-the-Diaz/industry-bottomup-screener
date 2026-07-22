import yfinance as yf
import pandas as pd

# List of fragmented industry companies (trucking/fleet management - like your Shoreline thesis)
tickers = ["WERN", "HTLD", "MRTN", "USX", "PTSI", "ARCB", "ODFL", "SAIA"]

# Empty list to store each company's data
results = []

for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    results.append({
        "Company": info.get("longName", ticker),
        "Ticker": ticker,
        "Market Cap ($M)": round(info.get("marketCap", 0) / 1_000_000, 1),
        "Revenue ($M)": round(info.get("totalRevenue", 0) / 1_000_000, 1),
        "EBITDA ($M)": round(info.get("ebitda", 0) / 1_000_000, 1),
        "Profit Margin (%)": round(info.get("profitMargins", 0) * 100, 2),
        "EV/EBITDA": round(info.get("enterpriseToEbitda", 0), 2),
    })

# Convert to table
df = pd.DataFrame(results)

# Sort by Market Cap smallest to largest (best roll-up targets first)
df = df.sort_values("Market Cap ($M)")

print("\n--- Fragmented Industry Roll-Up Screener ---\n")
print(df.to_string(index=False))
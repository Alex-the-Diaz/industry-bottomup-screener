import yfinance as yf  # Library that pulls live financial data from Yahoo Finance
import pandas as pd  # Library that organizes data into clean tables

# Ask the user to input tickers
print("\n--- Fragmented Industry Roll-Up Screener ---")
print("Enter stock tickers separated by commas (e.g. WERN, HTLD, MRTN):")
user_input = input("> ")

# Ask for industry name for the Excel file
print("What industry are you screening? (e.g. Trucking, HVAC, Auto Repair):")
industry_name = input("> ")

# Clean up the input and split into a list
tickers = [t.strip().upper() for t in user_input.split(",")]

print(f"\nFetching data for: {tickers}\n")

results = []  # Empty list to store each company's data

for ticker in tickers:  # Loop through each ticker one at a time
    stock = yf.Ticker(ticker)  # Tell yfinance which company to look up
    info = stock.info  # Pull all available financial data for that company

    results.append({  # Add this company's key metrics to the results list
        "Company": info.get("longName", ticker),  # Full company name
        "Ticker": ticker,  # Stock ticker symbol
        "Market Cap ($M)": round(info.get("marketCap", 0) / 1_000_000, 1),  # Total company value in millions
        "Revenue ($M)": round(info.get("totalRevenue", 0) / 1_000_000, 1),  # Annual revenue in millions
        "EBITDA ($M)": round(info.get("ebitda", 0) / 1_000_000, 1),  # Earnings before interest taxes depreciation
        "Profit Margin (%)": round(info.get("profitMargins", 0) * 100, 2),  # Net profit as percentage of revenue
        "EV/EBITDA": round(info.get("enterpriseToEbitda", 0), 2),  # Valuation multiple — lower = cheaper acquisition
    })

# Convert results list into a structured table
df = pd.DataFrame(results)

# Sort smallest to largest market cap — smallest are best roll-up targets
df = df.sort_values("Market Cap ($M)").reset_index(drop=True)

# --- Industry Summary Calculations ---
total_revenue = df["Revenue ($M)"].sum()
avg_margin = df["Profit Margin (%)"].mean()
avg_ev_ebitda = df[df["EV/EBITDA"] > 0]["EV/EBITDA"].mean()  # Ignore zeros
best_target = df[df["Market Cap ($M)"] > 0].iloc[0]  # Smallest valid market cap
consolidator = df["Market Cap ($M)"].idxmax()  # Largest market cap

summary_data = {
    "Metric": [
        "Industry",
        "Companies Screened",
        "Total Industry Revenue ($M)",
        "Average Profit Margin (%)",
        "Average EV/EBITDA Multiple",
        "Most Attractive Roll-Up Target",
        "Likely Industry Consolidator",
    ],
    "Value": [
        industry_name,
        len(df),
        round(total_revenue, 1),
        round(avg_margin, 2),
        round(avg_ev_ebitda, 2),
        f"{best_target['Company']} ({best_target['Ticker']}) — ${best_target['Market Cap ($M)']}M market cap",
        f"{df.loc[consolidator, 'Company']} ({df.loc[consolidator, 'Ticker']}) — ${df.loc[consolidator, 'Market Cap ($M)']}M market cap",
    ]
}

summary_df = pd.DataFrame(summary_data)

# --- Export to Excel ---
file_name = f"{industry_name.replace(' ', '_')}_RollUp_Screener.xlsx"

with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Company Data", index=False)  # Tab 1 — full company table
    summary_df.to_excel(writer, sheet_name="Industry Summary", index=False)  # Tab 2 — summary metrics

print(f"\n--- Industry Summary: {industry_name} ---")
print(summary_df.to_string(index=False))
print(f"\nFile saved as: {file_name}")
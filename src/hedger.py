import pandas as pd
from datetime import datetime
from src.black_scholes import bs_delta

def load_data(positions_file, market_file):
    """Load positions and market data from CSVs"""
    positions = pd.read_csv(positions_file)
    market = pd.read_csv(market_file, parse_dates=['Date'])
    return positions, market

def compute_delta_hedge(positions, market):
    """Compute daily delta hedges per underlying"""
    
    results = []

    # Loop through each date
    for date, daily_data in market.groupby('Date'):
        # Merge positions with market data
        merged = positions.merge(daily_data, on='Underlying', how='left')

        # Compute time to expiry in years
        merged['T'] = (pd.to_datetime(merged['Expiry']) - date).dt.days / 365

        # Compute delta per leg
        def calc_delta(row):
            S = row['Price']
            K = row['Strike']
            T = row['T']
            r = row['Rate']
            q = row.get('DividendYield', 0)
            sigma = row['ImpliedVol']
            option_type = row['Type']  # 'C' or 'P'
            delta = bs_delta(S, K, T, r, q, sigma, option_type)
            return delta * row['SideFactor'] * row['Contracts'] * 100

        merged['LegDelta'] = merged.apply(calc_delta, axis=1)

        # Aggregate net delta per underlying
        daily_delta = merged.groupby('Underlying')['LegDelta'].sum().reset_index()
        daily_delta['HedgeShares'] = -daily_delta['LegDelta']
        daily_delta['Date'] = date

        results.append(daily_delta)

    return pd.concat(results, ignore_index=True)

def main():
    positions_file = 'data/positions.csv'
    market_file = 'data/market_data.csv'

    positions, market = load_data(positions_file, market_file)
    hedge_df = compute_delta_hedge(positions, market)

    # Save daily hedges to CSV
    hedge_df.to_csv('data/daily_hedges.csv', index=False)
    print("Delta hedging calculation complete. Output saved to data/daily_hedges.csv")

if __name__ == "__main__":
    main()

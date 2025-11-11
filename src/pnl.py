import pandas as pd

def compute_hedge_pnl(daily_hedges_file):
    """
    Compute daily hedge PnL from delta hedges.
    
    Parameters
    ----------
    daily_hedges_file : str
        Path to CSV produced by hedger.py with columns:
        ['Date', 'Underlying', 'HedgeShares', 'LegDelta']
    
    Returns
    -------
    pnl_df : pd.DataFrame
        Daily hedge PnL per underlying and cumulative PnL
    """
    df = pd.read_csv(daily_hedges_file, parse_dates=['Date'])
    df.sort_values(['Underlying', 'Date'], inplace=True)

    df['PrevPrice'] = df.groupby('Underlying')['LegDelta'].shift(1)
    df['PrevPrice'] = df['PrevPrice'].fillna(0)

    # Hedge PnL = HedgeShares_prev * (Price_today - Price_prev)
    # We'll approximate LegDelta as hedge shares * price movement
    df['HedgePnL'] = df['HedgeShares'] * (df['LegDelta'] - df['PrevPrice'])

    # Cumulative PnL per underlying
    df['CumulativePnL'] = df.groupby('Underlying')['HedgePnL'].cumsum()

    return df[['Date', 'Underlying', 'HedgePnL', 'CumulativePnL']]

def main():
    daily_hedges_file = 'data/daily_hedges.csv'
    pnl_df = compute_hedge_pnl(daily_hedges_file)
    pnl_df.to_csv('data/hedge_pnl.csv', index=False)
    print("Hedge PnL calculation complete. Output saved to data/hedge_pnl.csv")

if __name__ == "__main__":
    main()

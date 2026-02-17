import yfinance as yf
import pandas as pd
import matplotlib 
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
os.makedirs('./visualisations/', exist_ok=True)
print(" Documents/projet_finance/scripts/visualisations/")

tickers = ["AAPL", "JPM", "MSFT"] 
data = yf.download(tickers, start="2022-01-01", end="2024-01-01", group_by='ticker')
print(data.columns)
print(f"   {len(data)} trading days downloaded")

all_data = []

for date in data.index:
    for ticker in tickers:
        all_data.append({
            'Date': date,
            'Ticker': ticker,
                'Open': data[ticker]['Open'].loc[date],      
                'High': data[ticker]['High'].loc[date],      
                'Low': data[ticker]['Low'].loc[date],        
                'Close': data[ticker]['Close'].loc[date],   
        })

df = pd.DataFrame(all_data)
print(f"DataFrame created: {len(df)} rows")
print(df.head(1000))
df.to_csv('_donnees_janvier_aapl_jpm.csv', index=False)

for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    print(f"\n--- {ticker} ---")
    print(f"Secteur: {info.get('sector')}")
    print(f"P/E Ratio: {info.get('trailingPE')}")
    print(f"Market Cap: {info.get('marketCap')}")
    print(f"Dividend Yield: {info.get('dividendYield')}")

def calculate_technical_indicators(df_group):
        df_group['MA20'] = df_group['Close'].rolling(window=20).mean()
        df_group['MA50'] = df_group['Close'].rolling(window=50).mean()
        delta = df_group['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df_group['RSI'] = 100 - (100 / (1 + rs))

        df_group['BB_Middle'] = df_group['Close'].rolling(window=20).mean()
        bb_std = df_group['Close'].rolling(window=20).std()
        df_group['BB_Upper'] = df_group['BB_Middle'] + (bb_std * 2)
        df_group['BB_Lower'] = df_group['BB_Middle'] - (bb_std * 2)
    
        return df_group

df_with_indicators = df.groupby('Ticker').apply(calculate_technical_indicators).reset_index(drop=True)
df_aapl = df_with_indicators[df_with_indicators['Ticker'] == 'AAPL']
df_jpm = df_with_indicators[df_with_indicators['Ticker'] == 'JPM']
df_msft = df_with_indicators[df_with_indicators['Ticker'] == 'MSFT']

def plot_indicators_for_ticker(df_ticker, ticker_name):

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle(f'Analyse Technique - {ticker_name}', fontsize=16)
    axes[0].plot(df_ticker['Date'], df_ticker['Close'], label='Close', color='black', linewidth=2)
    axes[0].plot(df_ticker['Date'], df_ticker['MA20'], label='MA20', color='blue', alpha=0.7)
    axes[0].plot(df_ticker['Date'], df_ticker['MA50'], label='MA50', color='red', alpha=0.7)
    axes[0].plot(df_ticker['Date'], df_ticker['BB_Middle'], label='BB Middle', color='orange', linestyle='--')
    axes[0].plot(df_ticker['Date'], df_ticker['BB_Upper'], label='BB Upper', color='green', linestyle='--')
    axes[0].plot(df_ticker['Date'], df_ticker['BB_Lower'], label='BB Lower', color='red', linestyle='--')
    axes[0].set_title(f'Prix et Moyennes Mobiles - {ticker_name}')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(df_ticker['Date'], df_ticker['RSI'], label='RSI', color='purple')
    axes[1].axhline(y=70, color='r', linestyle='--', alpha=0.5, label='Surachat (70)')
    axes[1].axhline(y=30, color='g', linestyle='--', alpha=0.5, label='Survente (30)')
    axes[1].set_title('RSI (Relative Strength Index)')
    axes[1].set_ylim(0, 100)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    png_path = f'./visualisations/technical_{ticker_name}.png'
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.show(block=True)

df_clean = df_with_indicators.dropna()

print("Rows before dropna:", len(df_with_indicators))
print("Rows after dropna:", len(df_clean))
print("\nFirst rows without NaN:")
print(df_clean[['Date', 'Ticker', 'Close', 'MA20', 'MA50', 'RSI']].head())
plot_indicators_for_ticker(df_aapl, 'AAPL')
plot_indicators_for_ticker(df_jpm, 'JPM')
plot_indicators_for_ticker(df_msft, 'MSFT')






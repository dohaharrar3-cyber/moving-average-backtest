import yfinance as yf 
import pandas as pd 
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
import os
os.makedirs('/Users/mac1708/Documents/projet_finance/visualisations/', exist_ok=True)

tickers=["AAPL","JPM","MSFT"]
INITIAL_CAPITAL = 10000
RISK_FREE_RATE = 0.04  
## Creation de la DataFrame : 
data=yf.download(tickers, start= "2022-01-01",end= "2024-01-01",group_by='ticker')
all_data=[]
for date in data.index:
    for ticker in tickers : 
        all_data.append({"Date":date ,
                         "Ticker":ticker,
                         "Close":data[ticker]['Close'].loc[date]
                        })
df=pd.DataFrame(all_data)        
print(df.head())

def calculate_technical_indicators(df):
    df["MA20"]=df['Close'].rolling(window=20).mean()
    df["MA50"]=df['Close'].rolling(window=50).mean()
    return df
df=df.groupby('Ticker').apply(calculate_technical_indicators).reset_index(drop=True)
df = df.dropna()

def add_signals(df):
    df['Signal']=0
    df.loc[df["MA20"]>df["MA50"],'Signal']= 1 ## Buy 
    df.loc[df["MA20"]<df["MA50"],'Signal']= -1 ## Sell 
    return df
df=df.groupby('Ticker').apply(add_signals).reset_index(drop=True)
print(df)

def simulate_portfolio(df):
    df['Daily_Return']=df['Close'].pct_change() ## calcul la variation en % entre chaque jour 
    df['Signal_Shifted']=df['Signal'].shift(1) 
    df['Strategy_Return']=df['Daily_Return']*df['Signal_Shifted']
    df['Portfolio_value']= INITIAL_CAPITAL * (1+ df['Strategy_Return']).cumprod() ## multiplie les valeurs i et i+1 entre elle 
    return df
df=df.groupby('Ticker').apply(simulate_portfolio).reset_index(drop=True)
print(df[['Date','Ticker','Close','Signal','Portfolio_value']].head(20))

def calculate_performance(df_ticker): ## Mesurer l'efficacité de la strategie 
    annual_return=df_ticker['Strategy_Return'].mean() * 252
    annual_volatility=df_ticker['Strategy_Return'].std() * np.sqrt(252)
    sharpe= (annual_return - RISK_FREE_RATE) / annual_volatility ## Ce que je gagne si je risque 

    rolling_max=df_ticker['Portfolio_value'].cummax()
    drawdown = (df_ticker['Portfolio_value']- rolling_max)/ rolling_max 
    max_drawdown= drawdown.min() ## La pire perte depuis le sommet (sommet a chaque jour ->cummax)
    total_return= (df_ticker['Portfolio_value'].iloc[-1]-10000)/10000

    print(f"\n {df_ticker['Ticker'].iloc[0]}") 
    print(f"Total Return   : {total_return:.2%}")
    print(f"Sharpe Ratio   : {sharpe:.2f}")
    print(f"Max Drawdown   : {max_drawdown:.2%}")
    
for ticker in ["AAPL","JPM","MSFT"]:
        df_ticker=df[df['Ticker']==ticker]
        calculate_performance(df_ticker)
               
    
def buy_hold(df):
     df['Buy_Hold_value']= INITIAL_CAPITAL*(df['Close']/df['Close'].iloc[0])
     return df
df=df.groupby('Ticker').apply(buy_hold).reset_index(drop=True)
print(df[['Date','Ticker','Close','Signal','Portfolio_value','Buy_Hold_value']])

for ticker in ["AAPL", "JPM", "MSFT"]:
    df_ticker = df[df['Ticker'] == ticker]
    bh_return = (df_ticker['Buy_Hold_value'].iloc[-1] - INITIAL_CAPITAL) / INITIAL_CAPITAL
    print(f"{ticker} Buy & Hold Return : {bh_return:.2%}") 
    
def plot_signals (df_ticker,ticker_name):
     fig,ax=plt.subplots(figsize=(14,6))
     ax.plot(df_ticker['Date'],df_ticker['Close'],color='black',linewidth=1.5,label='Price')
     buy=df_ticker[df_ticker['Signal']==1]
     ax.scatter(buy['Date'],buy['Close'],marker='^',color='green',s=50,label='Buy',zorder=5)
     sell = df_ticker[df_ticker['Signal']==-1]
     ax.scatter(sell['Date'],sell['Close'],marker='v',color='yellow',s=50,label='Sell',zorder=5)
     ax.set_title(f"Buy/Sell signals-{ticker_name}")
     ax.legend()
     ax.grid(True,alpha=0.3)
     plt.savefig(f'/Users/mac1708/Documents/projet_finance/visualisations/{ticker_name}_signals.png', 
            dpi=300, bbox_inches='tight')
     plt.show()
def plot_performances(df_ticker,ticker_name):
     fig,ax=plt.subplots(figsize=(14,6))
     ax.plot(df_ticker['Date'],df_ticker['Portfolio_value'],color='blue',label='MA Strategy')
     ax.plot(df_ticker['Date'],df_ticker['Buy_Hold_value'],color='red',label='Buy & Hold')
     ax.axhline(y=INITIAL_CAPITAL,color='black',linestyle='--',alpha=0.5,label='Initial Capital')
     ax.set_title(f'Strategy vs Buy & Hold -{ticker_name}')
     ax.legend()
     ax.grid(True,alpha=0.3)
     plt.savefig(f'/Users/mac1708/Documents/projet_finance/visualisations/{ticker_name}_performance.png', 
            dpi=300, bbox_inches='tight')
     plt.show()
def plot_drawdown(df_ticker,ticker_name):
    rolling_max=df_ticker['Portfolio_value'].cummax()
    drawdown = (df_ticker['Portfolio_value']- rolling_max)/ rolling_max 
    fig,ax=plt.subplots(figsize=(14,4))
    ax.fill_between(df_ticker['Date'],drawdown,0,color='red',alpha=0.4,label='Drawdown')
    ax.set_title(f'Drawdown-{ticker_name}')
    ax.legend()
    ax.grid(True,alpha=0.3)
    plt.savefig(f'/Users/mac1708/Documents/projet_finance/visualisations/{ticker_name}_drawdown.png', 
            dpi=300, bbox_inches='tight')
    plt.show()
df_aapl = df[df['Ticker'] == 'AAPL']
df_jpm = df[df['Ticker'] == 'JPM']
df_msft = df[df['Ticker'] == 'MSFT']     
for ticker in ['AAPL','MSFT','JPM']:
     df_ticker=df[df['Ticker']==ticker]
     plot_signals(df_ticker,ticker)
     plot_performances(df_ticker,ticker)
     plot_drawdown(df_ticker,ticker)







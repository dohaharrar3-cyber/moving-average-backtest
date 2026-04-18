# Moving Average Crossover — Backtesting Strategy

## What is this project ? 

Before risking real money on a trading strategy, 
quantitative analysts simulate it on historical data 
to measure its performance. This is called backtesting.

In this project, I built a backtesting system in Python to answer one simple question :
> Can a simple rule-based trading strategy beat doing nothing ?

## The Moving Average Crossover strategy : 

The strategy is based on two Moving Averages :

- MA20 = average closing price over the last 20 days
- MA50 = average closing price over the last 50 days
If MA20 crosses ABOVE MA50 -> Buy 
   MA20 crosses BELOW MA50  -> Sell 

## Data

- Assets : AAPL (Apple), JPM (JPMorgan), MSFT (Microsoft)
- Period : January 2022 → January 2024
- Source : Yahoo Finance via yfinance
- Starting capital : $10,000 per asset

## Performance Metrics

Three metrics are used to evaluate the strategy :

   ### Total Return
Did the strategy make or lose money overall ?
>Total Return = (Final Value - Initial Capital) / Initial Capital

   ### Sharpe Ratio
Was the return worth the risk taken ?
>Sharpe Ratio = (Annual Return - Risk Free Rate) / Annual Volatility

   ### Max Drawdown
What was the worst loss from a peak before recovering ?
>Max Drawdown = (Portfolio at trough - Portfolio at peak) / Portfolio at peak

## Results

AAPL (Apple)
Total Return : -38.16% | Sharpe Ratio : -0.93 | Max Drawdown : -45.30%

JPM (JPMorgan)
Total Return : -20.45% | Sharpe Ratio : -0.55 | Max Drawdown : -39.26%

MSFT (Microsoft)
Total Return : -44.53% | Sharpe Ratio : -1.07 | Max Drawdown : -58.57%

All three assets produced negative returns with negative Sharpe ratios.

## Strategy vs Buy & Hold

To evaluate whether the MA crossover strategy adds real value, I compared it against the simplest possible benchmark : Buy & Hold.

Buy & Hold means investing $10,000 on day 1 and never selling,regardless of market conditions.
Buy & Hold Value = $10,000 × (Price today / Price on day 1)

This benchmark answers a fundamental question in quantitative finance :
> Does the complexity of my strategy justify its existence ?
> Or would doing nothing have been more profitable ?

AAPL: MA Strategy : -38.16% | Buy & Hold : 25.40%

JPM : MA Strategy : -20.45% | Buy & Hold : 35.58%

MSFT : MA Strategy : -44.53% | Buy & Hold : 33.08%

On all three assets, the MA crossover strategy underperformed Buy & Hold.

## Why did the strategy fail ?

2022 was a bear market , technology stocks dropped significantly 
due to rising interest rates and macroeconomic uncertainty.

Moving Average Crossover strategies work well in trending markets but generate too many false signals in volatile, directionless markets.

In 2022, the market kept changing direction rapidly, causing the strategy to buy just before drops and sell just before recoveries.



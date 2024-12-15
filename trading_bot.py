import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

stock_symbol = 'AAPL'
data = yf.download(stock_symbol, start='2020-01-01', end='2024-01-01')

print(data.head())

# Short-term and long-term moving averages
short_window = 40
long_window = 100

data['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

data['signal'] = 0
data.iloc[short_window:, data.columns.get_loc('signal')] = np.where(data['short_mavg'].iloc[short_window:] > data['long_mavg'].iloc[short_window:], 1.0, 0.0)

data['position'] = data['signal'].diff()

initial_balance = 100000
balance = initial_balance
shares = 0
portfolio_value = []

for index, row in data.iterrows():
    if row['position'].item() == 1 and balance >= row['Close'].item():  # Buy condition
        shares += 1
        balance -= row['Close'].item()
    elif row['position'].item() == -1 and shares > 0:  # Sell condition
        shares -= 1
        balance += row['Close'].item()

    portfolio_value.append(balance + shares * row['Close'].item())

portfolio_value_df = pd.Series(portfolio_value, index=data.index)

plt.figure(figsize=(12, 8))
plt.plot(portfolio_value_df, label='Portfolio Value')
plt.title(f'{stock_symbol} Trading Bot Portfolio Value')
plt.xlabel('Date')
plt.ylabel('Portfolio Value (USD)')
plt.legend(loc='best')
plt.show()

final_balance = balance + shares * data['Close'].iloc[-1]
print(f"Final portfolio value: ${final_balance:.2f}")

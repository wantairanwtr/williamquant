import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
import tushare as tp

pro=tp.pro_api()
def data_now(now_tickers):
    for ticker_mod in now_tickers:
        print(ticker_mod)
        if not os.path.exists("stock_dfs/{}.csv".format(ticker_mod)):
            df=pro.daily(ts_code=str(ticker_mod),start_date="20160101",end_date="20181118")
            df.reset_index(inplace=True)
            df.set_index("trade_date",inplace=True)
            df.to_csv("stock_dfs/{}.csv".format(ticker_mod))
#choose the stock you like
tickers=["000001.SZ","000002.SZ"]
# data_now(tickers)

#put all selected stock into one DataFrame
def put_some_stock_price_into_one_df(df_tickers):
    some_stock_price=pd.DataFrame()
    print(some_stock_price)

    for count,ticker in enumerate(df_tickers):
        df=pd.read_csv("stock_dfs/{}.csv".format(ticker))
        df.set_index("trade_date",inplace=True)
        df.rename(columns={"close":ticker},inplace=True)
        df.drop(["index","ts_code","open","high","low","pre_close","change","pct_chg","vol","amount"],axis=1,inplace=True)
        if some_stock_price.empty:
            some_stock_price=df
        else:
            some_stock_price=some_stock_price.join(df,how="outer")
        print(count)
    some_stock_price.to_csv("CSI_selected_Closes.csv")
# put_some_stock_price_into_one_df(tickers)

#make data clean
df=pd.read_csv("CSI_selected_Closes.csv")
df.set_index("trade_date",inplace=True)
# # print(df.loc[np.int64("20160316"):np.int64("20160413")])
df.dropna(inplace=True)

#The basic financial calculation
returns_daily=df.pct_change()
# print(returns_daily.head())
returns_annual=returns_daily.mean()*250
# print(returns_annual)
cov_daily=returns_daily.cov()
# print(cov_daily)
# a=returns_daily-returns_daily.mean()
# a1=a["000001.SZ"]
# a2=a["000002.SZ"]
# print(a1.mul(a1).sum()/574)
# print(a1.mul(a2).sum()/574)
# print(a2.mul(a1).sum()/574)
# print(a2.mul(a2).sum()/574)
cov_annual=cov_daily*250

portfolio_return=[]
portfolio_volatility=[]
stock_weights=[]

#Make Portfolio
num_assets=len(tickers)
num_portfolio=1000

for single_portfolio in range(num_portfolio):
    weights=np.random.random(num_assets)
    weights=weights/weights.sum()
    # print(weights)
    # print("--------------------")
    # print(np.dot(weights,returns_annual))
    # print("--------------------")
    # print((returns_annual*weights).sum())
    returns=np.dot(weights,returns_annual)
    # print(returns)
    volatility=np.sqrt(np.dot(weights.T,np.dot(weights,cov_annual)))
    # print(volatility)
    portfolio_return.append(returns)
    portfolio_volatility.append(volatility)
    stock_weights.append(weights)
# print(portfolio_return)
# print(portfolio_volatility)
# print(stock_weights)

#Make the selected Super Portfolio into one dataframe
portfolio={"Return":portfolio_return,
           "Volatility":portfolio_volatility}
for counter,ticker in enumerate(tickers):
    portfolio[ticker+" weight"]=[Weight[counter] for Weight in stock_weights]
df_portfolio=pd.DataFrame(portfolio)
# print(df_portfolio.head())
df_portfolio.to_csv("big_big_data.csv")

plt.style.use("seaborn")
df_portfolio.plot.scatter(x="Volatility",y="Return",figsize=(10,8),grid=True)
plt.xlabel("Volatility / Std Deviation")
plt.ylabel("Expected Returns")
plt.title("Efficient Frontier")
plt.show()
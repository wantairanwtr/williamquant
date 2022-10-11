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
tickers=["000001.SZ","000002.SZ"]
# data_now(tickers)

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

df=pd.read_csv("CSI_selected_Closes.csv")
df.set_index("trade_date",inplace=True)
# # print(df.loc[np.int64("20160316"):np.int64("20160413")])
df.dropna(inplace=True)
returns_daily=df.pct_change()
# print(returns_daily.head())
returns_annual=returns_daily.mean()*250
# print(returns_annual)
cov_daily=returns_daily.cov()
print(cov_daily)
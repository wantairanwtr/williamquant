import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
tickers=[]
def put_some_stock_price_into_one_df():
    some_stock_price=pd.DataFrame()
    print(some_stock_price)

    for count,ticker in enumerate(tickers):
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
put_some_stock_price_into_one_df()
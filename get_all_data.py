import tushare as ts
import pickle
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
ts.set_token("4255f4cccadbf2360a413469a8301012e3a46208571ffef488db2d4c")
pro=ts.pro_api()
# df=pro.daily(ts_code="000001.SZ",start_date="20180101",end_date="20181118")
# print(df)

#Lastest CSI 300

#find and save Lastest CSI 300 and make it compatible with tushare pro API

def find_and_save_CSI_300():
    CSI_300_df_SH=pro.hs_const(hs_type='SH')
    CSI_300_df_SZ = pro.hs_const(hs_type='SZ')
    tickers1=CSI_300_df_SH["ts_code"].values
    tickers2 = CSI_300_df_SZ["ts_code"].values
    tickers=set()
    for ticker1 in tickers1:
        tickers.add(ticker1)
    for ticker2 in tickers2:
        tickers.add(ticker2)
    tickers_mod=list(tickers)
    # for ticker in tickers:
    #     if ticker[0] =="6":
    #         ticker=ticker[:-3]
    #         print(ticker)
    # print(tickers_mod)
    with open("CSI_tickers.pickle","wb") as f:
        pickle.dump(tickers_mod,f)
    return tickers_mod
# find_and_save_CSI_300()

#Use CSI_300 list to get data from tushare pro API

def get_data_from_tushare(reload_CSI_300=False):
    if reload_CSI_300:
        tickers_mod=find_and_save_CSI_300()
    else:
        with open("CSI_tickers.pickle","rb") as f:
            tickers_mod=pickle.load(f)
    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")
    for ticker_mod in tickers_mod:
        print(ticker_mod)
        if not os.path.exists("stock_dfs/{}.csv".format(ticker_mod)):
            df=pro.daily(ts_code=str(ticker_mod),start_date="20160101",end_date="20181118")
            df.reset_index(inplace=True)
            df.set_index("trade_date",inplace=True)
            df.to_csv("stock_dfs/{}.csv".format(ticker_mod))
        else:
            print("We already have{}".format(ticker_mod))
# get_data_from_tushare()

#Put all stock close price into one dataframe

def put_all_stock_price_into_one_df():
    with open("CSI_tickers.pickle","rb") as f:
        tickers=pickle.load(f)
    all_stock_price=pd.DataFrame()
    for count,ticker in enumerate(tickers):
        df=pd.read_csv("stock_dfs/{}.csv".format(ticker))
        df.set_index("trade_date",inplace=True)
        df.rename(columns={"close":ticker},inplace=True)
        df.drop(["index","ts_code","open","high","low","pre_close","change","pct_chg","vol","amount"],axis=1,inplace=True)
        if all_stock_price.empty:
            all_stock_price=df
        else:
            all_stock_price=all_stock_price.join(df,how="outer")
        print(count)
    all_stock_price.to_csv("CSI_300_Joined_Closes.csv")
# put_all_stock_price_into_one_df()

#calculate,save and plot pearson correlation heatmap

def calculate_save_and_plot_pearson_correlation_heatmap():
    df=pd.read_csv("CSI_300_Joined_Closes.csv")
    df.drop(["trade_date"], axis=1, inplace=True)
    # df["000831.SZ"].plot()
    # plt.show()
    df_corr=df.pct_change().corr()
    # print(df_corr.head())
    # df_corr.to_csv("CSI_300_pct_change_corr.csv")
    data=df_corr.values
    # print(data.shape)
    fig=plt.figure()
    ax=fig.add_subplot(111)
    heatmap=ax.pcolor(data,cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(0.5,data.shape[0]+0.5,step=1),minor=False)
    ax.set_yticks(np.arange(0.5,data.shape[1]+0.5,step=1),minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_xticklabels(df_corr.columns)
    ax.set_yticklabels(df_corr.index)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()
calculate_save_and_plot_pearson_correlation_heatmap()
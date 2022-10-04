import tushare as ts
import pickle
import os
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
get_data_from_tushare()
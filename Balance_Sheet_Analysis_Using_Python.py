import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

#Set max rows/columns/width
pd.set_option("display.max_rows",999)
pd.set_option("display.max_columns",999)
pd.set_option("display.width",999)
# Firstly,import ouer data
df=pd.read_excel("RedHat.xlsx")
df.dropna(how="all",inplace=True)
# print(df)
index_PL=df.loc[df["Data provided by SimFin"]=="Profit & Loss statement"].index[0]
index_BS=df.loc[df["Data provided by SimFin"]=="Balance Sheet"].index[0]
index_CF=df.loc[df["Data provided by SimFin"]=="Cash Flow statement"].index[0]
df_PL=df.iloc[index_PL:index_BS-2,1:]
df_PL.columns=df_PL.iloc[0]
df_PL.set_index("in million USD",inplace=True)
df_PL.fillna(0,inplace=True)
df_PL=df_PL[1:]
# print(df_PL)
df_BS=df.iloc[index_BS-1:index_CF-3,1:]
df_BS.columns=df_BS.iloc[0]
df_BS.set_index("in million USD",inplace=True)
df_BS.fillna(0,inplace=True)
df_BS=df_BS[1:]
# print(df_BS)
df_CF=df.iloc[index_CF-2:,1:]
df_CF.columns=df_CF.iloc[0]
df_CF.set_index("in million USD",inplace=True)
df_CF.fillna(0,inplace=True)
df_CF=df_CF[1:]
# print(df_CF)
# df_PL.to_pickle("RedHat_PL.pkl")
# df_BS.to_pickle("RedHat_BS.pkl")
# df_CF.to_pickle("RedHat_CF.pkl")
df_PL=df_PL.T
plt.rcParams["figure.figsize"]=[15,10]
df_PL.plot()
plt.show()
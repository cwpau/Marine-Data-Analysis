
#gets csvs from qgis interesections and remove duplcated ones
import os
import tkinter as tk
import pandas as pd #pandas==1.1.4 or 1.1.5
from tkinter.filedialog import askopenfilename
from tkinter import filedialog as fd
from timebudget import timebudget
from datetime import datetime
import re
import numpy as np
from pandas_profiling import ProfileReport


def readfiles():
    root = tk.Tk()
    root.withdraw()
    filesopened = fd.askopenfilenames(parent=root, title='Choose the files')
    root.destroy()
    df = pd.DataFrame()
    for filesname in filesopened:
        if "GateSTV" in filesname:
            df_trash = pd.read_csv(filesname)
            a = filesname.partition('int')[2].partition('_')[2].partition('_')[0]
        elif "Gate2" in filesname:
            df_gate2 = pd.read_csv(filesname)
            b = filesname.partition('int')[2].partition('_')[2].partition('_')[0]

    if a==b:
        return df_gate2, df_trash, filesname.partition('int')[2].partition('_')[2].partition('_')[0]
    else:
        print("seems wrong pairs of files are selected, dates are not the same")
if __name__ == "__main__":
    rootpath = os.getcwd()+"/data/csvs/int_"

    datelist = pd.date_range(start='2021-10-31', end='2021-12-15', freq='d').to_list()
    datelist = [d.strftime('%Y-%m-%d') for d in datelist]

    empty= []
    df_gate1 = pd.DataFrame()
    df_gate2 = pd.DataFrame()
    df_gateSTV = pd.DataFrame(empty)

    for date in datelist:
        #@some function
        for gate in ["Gate1", "Gate2", "GateSTV"]:
            path = rootpath+date+"__"+gate+".csv"
            # print(path)
            
            if gate == "Gate1":
                dftemp=pd.read_csv(path)
                df_gate1=pd.concat([df_gate1,dftemp])

            elif gate == "Gate2":
                dftemp=pd.read_csv(path)
                stvpath = rootpath+date+"__GateSTV.csv"
                dftempstv = pd.read_csv(stvpath)

                # dftemp["Ship Type_Length"] = "STV" 
                dftemp["Ship Type_Length"].mask(dftemp['Track ID'].isin(dftempstv['Track ID']), "STV", inplace=True)
                print(dftemp)
                df_gate2 = pd.concat([df_gate2,dftemp])
            else:
                continue
    # path = "/Users/wilsoncwpau/Library/CloudStorage/OneDrive-3vj4cv/QGIS_Marine/data/csvs/int_2021-10-31__Gate2.csv"
    # df=pd.read_csv(path)
    print(df_gate2)

    print(df_gate2.columns)
    df_gate1["Hour"]=pd.to_datetime(df_gate1["Nearest"]).dt.round(freq='H').dt.hour
    df_gate2["Hour"]=pd.to_datetime(df_gate2["Nearest"]).dt.round(freq='H').dt.hour

    df_gate1.to_csv('g1.csv')
    df_gate2.to_csv('g2.csv')

    table1=df_gate1.groupby(by=["Ship Type_Length","Hour"], as_index=False).size()
    table1.to_csv('table1.csv')
    table2=df_gate2.groupby(by=["Ship Type_Length","Hour"], as_index=False).size()
    table2.to_csv('table2.csv')
    # a=readfiles()
    # dfgate = a[0]
    # dftrash = a[1]
    # filename = a[2]
    # # print(dfgate, dftrash)

    # # print(dfgate.nunique())

    # dfnew = dfgate[~dfgate['Track ID'].isin(dftrash['Track ID'])]
    # dfnew = dfnew.iloc[:, :7]
    # # print(dfnew.nunique())

    # # print(dfnew)
    # dfnew.to_csv(f"{filename}_shipsthroughgate2.csv")
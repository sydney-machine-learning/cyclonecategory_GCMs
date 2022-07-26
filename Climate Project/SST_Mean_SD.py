import numpy as np
import pandas as pd
from math import *
import xarray as xr
from datetime import datetime,timedelta
from matplotlib import pyplot as plt

def sst_mean_std(csv_path, out_path):
    df=pd.read_csv(csv_path)
    df=df.drop(columns='Unnamed: 0')
    for index,row in df.iterrows():
        sub=0
        for weeks in range(1,5):
            sum1=0
            for days in range(1,8):
                sub+=1
                su=str(sub)
                sum1+=df[su][index]
                
            sum1=sum1/7
            s='Week'+'_'+ str(weeks)+'_'+ 'Mean'
            df.loc[index,s]=sum1
    for index,row in df.iterrows():
        sub1=0
        sub2=0
        for weeks in range(1,5):
            sum1=0
            sum2=0
            for days in range(1,8):
                sub1+=1
                su=str(sub1)
                sum1+=df[su][index]
                
            sum1=sum1/7
            for days in range(1,8):
                sub2+=1
                su=str(sub2)
                sum2+=(df[su][index]-sum1)*(df[su][index]-sum1)
            sum2=sum2/7
            s='Week'+'_'+ str(weeks)+'_'+ 'SD'
            df.loc[index,s]=sqrt(sum2)
    dict={0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[],21:[],22:[],23:[],24:[],25:[],26:[],27:[],28:[],29:[],30:[],31:[],32:[],33:[],34:[],35:[],36:[],37:[],38:[],39:[],40:[]} 
    for index,row in df.iterrows():
        add=dict[df["No. of Cycl"][index]]
        add.append(df["Speed(knots)"][index])
    df.sort_values(["No. of Cycl"],axis=0, ascending=True,inplace=True,na_position='first')
    df['Avg_Wind_speed']=""
    df['Deviation_Wind_speed']=""
    for i in range(1,39):
        c=0
        d=0
        if(len(dict[i])!=0):
            for j in range(0,len(dict[i])):
                c=c+dict[i][j]
                d=d+dict[i][j]*dict[i][j]
            c=c/len(dict[i])
            d=d/len(dict[i])
            for index,row in df.iterrows():
                if(df['No. of Cycl'][index]==i):
                    df.loc[index,'Avg_Wind_speed']=c
                    df.loc[index,'Deviation_Wind_speed']=sqrt(d-c*c)
                    break
    df = df.reset_index(drop=True)

    df.to_csv(out_path)

sst_mean_std('/Users/somadityasingh/Climate Project/South_Pacific.csv', "SP_Mean_SD.csv")
sst_mean_std('/Users/somadityasingh/Climate Project/South_Indian.csv', "SI_Mean_SD.csv")
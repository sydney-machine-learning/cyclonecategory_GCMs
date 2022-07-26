import pandas as pd
import xarray as xr
from datetime import datetime,timedelta
from matplotlib import pyplot as plt
from netCDF4 import Dataset
import pathlib

def extract_data(nc_path, url_path, csv_path):

    ds= Dataset(nc_path)
    url_1= url_path
    df_1 = pd.read_csv(url_1, sep=',')
    df_1['Time']=pd.to_datetime(df_1['Time'],format='%Y%m%d%H')
    time=ds.variables['time'][:]
    lat=ds.variables['latitude'][:]
    lon=ds.variables['longitude'][:]
    sst=ds.variables['sst']
    sd=ds.variables['expver']
    df_1['Time']=pd.to_datetime(df_1['Time'],format='%Y%m%d%H')
    time=ds.variables['time'][:]
    lat=ds.variables['latitude'][:]
    lon=ds.variables['longitude'][:]
    sst=ds.variables['sst']

    intial=1900010100
    initial_date=pd.to_datetime(intial,format='%Y%m%d%H')
    df_1["diff"]=df_1['Time']-initial_date
    df_1['total_1']=(df_1['diff']/timedelta(seconds=1))/3600
    df_1['sst_1']=""

    for index,row in df_1.iterrows():
        latitude=row['lat_tenth']
        longitude=row['lon_tenth']
        total_1=row['total_1']

        
        diff_lat=(lat-latitude)**2
        diff_lon=(lon-longitude)**2
        diff_time=(time-total_1)**2

        
        min_lat=diff_lat.argmin()
        min_lon= diff_lon.argmin()
        min_time=diff_time.argmin()

        
        df_1.loc[index,'sst_1']=sst[min_time,0,min_lat,min_lon]
    df_1.to_csv('Subs_SP.csv',index=False)
    with open('Subs_SP.csv','r') as in_file, open(csv_path,'w') as out_file:
    
      seen = set() 
      
      for line in in_file:
          if line in seen: 
            continue 

          seen.add(line)
          out_file.write(line)

    df = pd.read_csv(csv_path)

    for index,row in df.iterrows():
          start=df['total_1'][index]
          for days in range(1,31):
                start=start-24*days

                latitude=df['lat_tenth'][index]
                longitude=df['lon_tenth'][index]

                diff_lat=(lat-latitude)**2
                diff_lon=(lon-longitude)**2
                diff_time=(time-start)**2

                min_lat=diff_lat.argmin()
                min_lon= diff_lon.argmin()
                min_time=diff_time.argmin()

                df.loc[index,days]=sst[min_time,0,min_lat,min_lon] 

    df = df.reset_index(drop=True)
    df.to_csv(csv_path)

extract_data(r'/Users/somadityasingh/SP_SST.nc' , "https://raw.githubusercontent.com/sydney-machine-learning/cyclonedatasets/main/SouthIndian-SouthPacific-Ocean/South_pacific_hurricane.csv", "South_Pacific.csv")
extract_data(r'/Users/somadityasingh/SI_SST.nc' , "https://raw.githubusercontent.com/sydney-machine-learning/cyclonedatasets/main/SouthIndian-SouthPacific-Ocean/South_indian_hurricane.csv", "South_Indian.csv")
#Importing Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from matplotlib.pyplot import figure
from keras.layers import LSTM
from keras.layers import ConvLSTM2D
from keras.layers import Flatten
from numpy import array
from sklearn.preprocessing import StandardScaler
from numpy import hstack

#Import Raw Data and convert it to CSV 

url = "https://raw.githubusercontent.com/rohitash-chandra/CMTL_dynamictimeseries/master/SouthIndianOcean/updated_rawdata/southindianocean_jtwc.csv"
df = pd.read_csv(url, sep=',',header = None,error_bad_lines=False)
df.columns = ['ID','Date','Longitude','Latitude','Speed']
df['Category'] = df['Speed'].apply(lambda x: 1 if x<=27 else 2  if x<=33 and x> 27 else 3 if x<=47 and x> 33 else 4 if x<=63 and x> 47 else 5 if x<=89 and x> 63 else 6 if x<=119 and x>89 else 7 )
df = df.drop(['Date'], axis = 1)
df.to_csv('adjusted.csv')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')


#Making starting point of every cyclone same, spatial bias removed

id = 1
x0 = df['Longitude'][0]
y0 = df['Latitude'][0]
df['Longitude'][0] = 0
df['Latitude'][0] = 0

for i in range(1, df.shape[0]):
        if df['ID'][i] == id :
            df['Longitude'][i] = df['Longitude'][i] - x0
            df['Latitude'][i] = df['Latitude'][i] - y0
        else:
            x0 = df['Longitude'][i]
            y0 = df['Latitude'][i]
            df['Longitude'][i] = 0
            df['Latitude'][i] = 0
            id = df['ID'][i]
    
# Extracting speed data from Dataset and creating Multivariate Dataset of Track and Speed

speed = array(df['Speed'])
speed=speed.reshape(len(speed),1)

longitude=array(df['Longitude'])
longitude=longitude.reshape(len(longitude),1)

latitude=array(df['Latitude'])
latitude=latitude.reshape(len(latitude),1)

category=array(df['Category'])

dataset=hstack((longitude,latitude,speed,speed))

def rmse(pred, actual):
    temp = np.sqrt(((pred-actual)**2).mean())
    return temp

def cat_calc(tsd): 
    output=np.empty(len(tsd))
    for i in range(len(tsd)):
        if tsd[i]<=27:
            output[i]=1
        elif tsd[i]>27 and tsd[i]<=33:
            output[i]=2
        elif tsd[i]>33 and tsd[i]<=47:
            output[i]=3
        elif tsd[i]>47 and tsd[i]<=63:
            output[i]=4
        elif tsd[i]>63 and tsd[i]<=89:
            output[i]=5
        elif tsd[i]>89 and tsd[i]<=119:
            output[i]=6
        else:
            output[i]=7
    return output

n_steps_in=3
univariate=False
n_steps_out=1

if univariate==True:
    n_features=1
    dataset=speed
else: 
    n_features=3

def split_seq(univariate, sequence, n_steps_in,n_steps_out):
    if univariate==True:
        X, y =[],[]
        for i in range(len(sequence)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix+n_steps_out
            # check if we are beyond the sequence
            if out_end_ix > len(sequence)-1:
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return np.array(X), np.array(y)


    else:

        # split a Multivariate sequence into samples
        X, y = list(), list()
        for i in range(len(sequence)):
            # find the end of this pattern
            end_ix = i + n_steps_in
            out_end_ix = end_ix + n_steps_out-1
            # check if we are beyond the dataset
            if out_end_ix > len(sequence):
                break
            # gather input and output parts of the pattern
            seq_x, seq_y = sequence[i:end_ix, :-1], sequence[end_ix-1:out_end_ix, -1]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)

# From Dataset DataFrame, Separate and Prepare (Split and make 3D) Test and Train Data 

train = dataset[0:10000]
test = dataset[10000:20167]

x_train, y_train = split_seq(univariate, train, n_steps_in,n_steps_out)
x_test, y_test = split_seq(univariate, test, n_steps_in,n_steps_out)

x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], n_features))
print(x_train.shape)

x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], n_features))
print(x_test.shape)

y_train = y_train.reshape((y_train.shape[0], y_train.shape[1]))
print(y_train.shape)

# Defining and Fitting the Conv LSTM Network 

#Define the Model
model=Sequential()
model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
model.add(LSTM(100, activation='relu'))
model.add(Dense(n_steps_out))
model.compile(optimizer='adam', loss='mse')
model.summary()

y_test = y_test.reshape((y_test.shape[0], y_test.shape[1]))
print(y_test.shape)

#Fit the Model 
model.fit(x_train,y_train,epochs=100,verbose=0)

#Predict with the Fitted Model 
y_train_predicted=model.predict(x_train)
y_test_predicted=model.predict(x_test)

#Calculate the Categories for Train 
actual_cat_train=cat_calc(speed[2:10000])
predicted_cat_train=cat_calc(y_train_predicted)

#Calculate the Categories for Test
actual_cat_test=cat_calc(speed[10002:20167])
predicted_cat_test=cat_calc(y_test_predicted)

#Displaying Train and Test Accuracies 

#Check RMSE
train_acc=rmse(predicted_cat_train,actual_cat_train)
test_acc=rmse(predicted_cat_test,actual_cat_test)

print(train_acc, 'is the RMSE for the Train Data') 
print(test_acc, 'is the RMSE for the Test Data')

i=1
while(i<36):
    max_cat=0
    for j in range(len(df['ID'])):
        if (df['ID'][j]==i):
            if (df['Category'][j]>max_cat):
                max_cat=df['Category'][j]
                
    for j in range(len(df['ID'])):
        if(df['ID'][j]==i):
            df['Category'][j]=max_cat
    
    i=i+1
        
    
plot_long=np.zeros(len(df['ID']))
plot_lat=np.zeros(len(df['ID']))
plot_cat=np.zeros(len(df['ID']))

plot_long[0]=df['Longitude'][0]
plot_lat[0]=df['Latitude'][0]
plot_cat[0]=df['Category'][0]



for i in range(1,len(df['ID'])):
    if df['ID'][i]!=df['ID'][i-1]:
        plot_long[i]=df['Longitude'][i]
        plot_lat[i]=df['Latitude'][i]
        plot_cat[i]=df['Category'][i]

plot_long=plot_long[plot_long!=0]
plot_lat=plot_lat[plot_lat!=0]
plot_cat=plot_cat[plot_cat!=0]


dataset = pd.DataFrame({'Longitude': plot_long, 'Latitude': plot_lat, 'Category':plot_cat})[0:20]
df_geo=gpd.GeoDataFrame(dataset,geometry= gpd.points_from_xy(dataset.Longitude,dataset.Latitude))
world_data=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
plt.rcParams["figure.figsize"] = (20,20)
ax = world_data.plot(color='lightblue', edgecolor='black')
df_geo.plot(column='Category',ax=ax, legend=True, legend_kwds={'label': "Category of Cyclone",'orientation': "horizontal"})
plt.show()

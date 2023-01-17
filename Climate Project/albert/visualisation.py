import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

CSV_PATH = "./albert/SP_with_ids.csv"


df = pd.read_csv(CSV_PATH)

def cyclone_speed_overview():
    print("Average cyclone observation speed")
    print(np.mean(df["Speed(knots)"]))

    print("Highest observed cyclone observation speed")
    print(np.max(df["Speed(knots)"]))

    sns.displot(df, x="Speed(knots)")
    plt.show()


def tempsForExtremeCyclones():

    # filter for wind speeds greater than 100 knots
    extreme_df = df.loc[df["Speed(knots)"] >= 100]
    
    print("Number of cyclones with peak wind speeds above 100 knots: ")
    extreme_ids = extreme_df['id'].unique()
    print(len(extreme_ids))

    # observe differences in temperature between SST
    local_df = df
    local_df['is_extreme'] = local_df["id"].apply(lambda id: id in extreme_ids)
    local_df['peak_wind'] = df.groupby('id')['Speed(knots)'].transform('max')


    sns.displot(df,x="Week_4_Mean", hue='is_extreme',kind="kde", fill=True)
    plt.show()

    # take only the first observation for each cyclone -- 
    new_df = pd.DataFrame(columns=local_df.columns)
    for cyclone_id in df['id'].unique():
        row = local_df.query('id == ' + str(cyclone_id) ).head(1)
        new_df = pd.concat([new_df, row])


    sns.relplot(x="Week_4_Mean", y="peak_wind", data=new_df);
    model = LinearRegression()
    model.fit(new_df["Week_4_Mean"].values.reshape(-1,1), new_df["peak_wind"].values.reshape(-1,1))

    predictions = model.predict(new_df["Week_4_Mean"].values.reshape(-1,1))


    print(model.coef_)

    plt.scatter(new_df["Week_4_Mean"], new_df["peak_wind"], color="black")
    plt.plot(new_df["Week_4_Mean"], predictions, color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())

    plt.show()



    plt.show()

 
cyclone_speed_overview()
tempsForExtremeCyclones()



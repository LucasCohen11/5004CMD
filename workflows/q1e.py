from tester import compareImplementations as compare
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import dask.dataframe as dd

def q1e_sequential():
    df = pd.read_csv(r'../data/Trips_Full Data.csv')
    cols = [x for x in df.columns if 'Trips ' in x]
    data = df[cols].sum()
    data.plot(kind="bar")
    plt.title("Total Trips by Distance Bin")
    plt.xlabel("Trip Distance Bin")
    plt.ylabel("Total Number of Trips")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def q1e_Dask():
    df = dd.read_csv(r'../data/Trips_Full Data.csv')

    cols = [col for col in df.columns if 'Trips ' in col]

    data = df[cols].sum().compute()

    data.plot(kind="bar")
    plt.title("Total Trips by Distance Bin")
    plt.xlabel("Trip Distance Bin")
    plt.ylabel("Total Number of Trips")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    print("Result of comparing question 1e")
    compare(q1e_sequential,q1e_Dask)
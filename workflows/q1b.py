from tester import compareImplementations as compare
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dask.dataframe as dd


def q1b_sequential():
    df = pd.read_csv(r'../data/National_only.csv')
    df.drop_duplicates(inplace=True)
    qualifying_shorter_trips = df[df['Number of Trips 10-25']>10000000]['Date']
    qualifying_longer_trips = df[df['Number of Trips 50-100']>10000000]['Date']
    
    #this is just so that optimizations don't skip the code for being unused
    [x for x in qualifying_shorter_trips if x not in qualifying_longer_trips.values]

def q1b_Dask():
    df = dd.read_csv(r'../data/National_only.csv')
    df.drop_duplicates()
    qualifying_shorter_trips = df.query('`Number of Trips 10-25` > 10000000')['Date'].compute()
    qualifying_longer_trips = df.query('`Number of Trips 50-100` > 10000000')['Date'].compute()
    [x for x in qualifying_shorter_trips if x not in qualifying_longer_trips.values]

if __name__ == "__main__":
    print("Result of comparing question 1b")
    compare(q1b_sequential,q1b_Dask)
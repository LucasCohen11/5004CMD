from tester import compareImplementations as compare
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dask.dataframe as dd
import numpy as np
from dask_ml.linear_model import LinearRegression
from dask_ml.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score




def parse_ranges_to_dict(ranges):
        range_dict = {}
        for r in ranges:
            if '<' in r:
                start = 0
                end = float(r.split('<')[-1])
            elif '>=' in r:
                start = float(r.split('>=')[-1])
                end = start*2
            elif '-' in r:
                start, end = map(float, r.split('-'))
            else:
                raise ValueError(f"Invalid range format: {r}")
            range_dict[r] = (start, end)
        return range_dict
    
    
    
    
def q1d_sequential():
    df = pd.read_csv(r'../data/National_only.csv').dropna()
    df.drop_duplicates(inplace=True)
        
    #columns that represent trip amounts per distance bin
    cols = [x for x in df.columns if 'Number of Trips ' in x]

    #Minimum and Maximum distance to belong to a specific bin
    ranges = parse_ranges_to_dict([x.split(' ')[-1] for x in cols]).values()
    distance_bins={}
    for cname,(start,end) in zip(cols,ranges):
        distance_bins[cname]=(start+end)/2
    
    new_rows = []

    # Iterate through each row in df
    for _, row in df.iterrows():
        # For each bin, create a new row with the corresponding distance and number of trips
        for col in cols:
            new_row = {
                'Distance': distance_bins[col],
                'Trips': row[col]
            }
            new_rows.append(new_row)

    # Create a new dataframe with the new rows
    df_new = pd.DataFrame(new_rows)
    X = df_new[['Distance']].values  
    y = df_new['Trips'].values       

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=22,shuffle=True)

    model = LinearRegression()

    # Fit the model on the training data
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Use scikit-learn metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("MSE:", mse)
    print("R²:", r2)
        

def q1d_Dask():
    df = dd.read_csv(r'../data/National_only.csv').dropna()
    df.drop_duplicates().compute()
    cols = [x for x in df.columns if 'Number of Trips ' in x]
    #Minimum and Maximum distance to belong to a specific bin
    ranges = parse_ranges_to_dict([x.split(' ')[-1] for x in cols]).values()
    distance_bins={}
    for cname,(start,end) in zip(cols,ranges):
        distance_bins[cname]=(start+end)/2

    meta = [('bin', 'object'), ('Trips', 'float64')]
    
    # perform the melt operation on each partition of the Dask DataFrame.
    df_long = df.map_partitions(
        lambda df_part: df_part.melt( value_vars=cols, var_name='bin', value_name='Trips'),
        meta=meta
    )

    # Map the bin labels to their corresponding distances using the dictionary
    df_long['Distance'] = df_long['bin'].map(distance_bins,meta=('bin','float64'))


    df_new_dask = df_long[['Distance', 'Trips']]
    df_new_dask.compute()
        
    # Convert the predictors and response to Dask arrays.
    X = df_new_dask[['Distance']].to_dask_array(lengths=True)
    y = df_new_dask['Trips'].to_dask_array(lengths=True)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=22)

    model = LinearRegression()

    # Fit the model on the training data
    model.fit(X_train, y_train)
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    # Compute the predictions and true values
    y_pred_np = y_pred.compute()
    y_test_np = y_test.compute()

    # Use scikit-learn metrics
    mse = mean_squared_error(y_test_np, y_pred_np)
    r2 = r2_score(y_test_np, y_pred_np)

    print("MSE:", mse)
    print("R²:", r2)


    

if __name__ == "__main__":
    print("Result of comparing question 1d")
    compare(q1d_sequential,q1d_Dask)
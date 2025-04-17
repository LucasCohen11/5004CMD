import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


import dask.dataframe as dd


from tester import compareImplementations as compare
#As stated before, we can use only national data
#without loss of information
def q1a_sequential():
    df = pd.read_csv(r"../data/National_only.csv")

    #We want the mean number of people per week staying at home
    #so we group by week and take the mean
    mean_staying =df[['Population Staying at Home','Week']].groupby(by='Week').mean(numeric_only=True)
    plt.figure(figsize=(12, 6))
    mean_staying.plot(marker='o', color='teal')
    plt.title('Average Number of People Staying at Home per Week')
    plt.xlabel('Week Number')
    plt.ylabel('Amount of people')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    
    #Now for how far people travel when they don't stay at home
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


    cols = [x for x in df.columns if 'Number of Trips ' in x]
    ranges = parse_ranges_to_dict([x.split(' ')[-1] for x in cols]).values()
    distance_bins={}
    for cname,(start,end) in zip(cols,ranges):
        distance_bins[cname]=(start+end)/2

    
    grouped_by_week_sum = df.groupby('Week').sum(numeric_only=True)

    # Calculate total distance traveled per week
    total_distance_per_week = (grouped_by_week_sum[cols] * list(distance_bins.values())).sum(axis=1)

    # Calculate average distance traveled per person who did not stay at home
    avg_distance_per_person = total_distance_per_week / grouped_by_week_sum['Population Not Staying at Home']





def q1a_Dask():
    df = dd.read_csv(r'../data/National_only.csv')
    mean_staying =df[['Population Staying at Home','Week']].groupby(by='Week').mean(numeric_only=True).compute()
    plt.figure(figsize=(12, 6))
    mean_staying.plot(marker='o', color='teal')
    plt.title('Average Number of People Staying at Home per Week')
    plt.xlabel('Week Number')
    plt.ylabel('Amount of people')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    #Now for how far people travel when they don't stay at home
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


    cols = [x for x in df.columns if 'Number of Trips ' in x]
    ranges = parse_ranges_to_dict([x.split(' ')[-1] for x in cols]).values()
    distance_bins={}
    for cname,(start,end) in zip(cols,ranges):
        distance_bins[cname]=(start+end)/2

    
    grouped_by_week_sum = df.groupby('Week').sum(numeric_only=True)

    # Calculate total distance traveled per week
    total_distance_per_week = (grouped_by_week_sum[cols] * list(distance_bins.values())).sum(axis=1)

    # Calculate average distance traveled per person who did not stay at home
    avg_distance_per_person = total_distance_per_week / grouped_by_week_sum['Population Not Staying at Home']
    avg_distance_per_person.compute()
    
    

if __name__ == "__main__":
    print("Result of comparing question 1a")
    compare(q1a_sequential,q1a_Dask)
    print("Done!")
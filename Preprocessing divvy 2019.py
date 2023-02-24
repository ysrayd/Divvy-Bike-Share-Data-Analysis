# Import Dependencies
from matplotlib import pyplot as plt
import scipy.stats as stats
from scipy.stats import linregress
import numpy as np
from sklearn import datasets
import pandas as pd
import requests
import json
import os
import gmaps

# Import data file
divvy_df = pd.read_csv('C:/Users/HP/Desktop/DIVVY DATA FULL/Divvy_2019.csv')
divvy_df.shape

# Display sample of dataframe
divvy_df.head()

# Remove null rows (if needed)
divvy_df.dropna("columnname",axis=1, inplace=True)
divvy_df.shape

# Find column names
divvy_df.columns

# Convert birthyear to age
divvy_df['AGE'] = (2019 - divvy_df['BIRTH YEAR'])
divvy_df.head()

# Create bins for age
bins = [10, 20, 30, 40, 50, 60, 70, 80, 90]
# Create the names for the bins
group_names = ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89"]
divvy_df["Age Group"] = pd.cut(divvy_df["AGE"], bins, labels=group_names, include_lowest=True)
divvy_df.head()

divvy_df['time difference'] = ((pd.to_datetime(divvy_df['STOP TIME']) - 
                            pd.to_datetime(divvy_df['START TIME']))
                                .dt.total_seconds() / 60)
divvy_df

# Convert date columns to datetime format
divvy_df['START TIME'] = pd.to_datetime(divvy_df['START TIME'])
divvy_df['STOP TIME'] = pd.to_datetime(divvy_df['STOP TIME'])


# Split date from time and create columns
divvy_df['START DATE'] = divvy_df['START TIME'].dt.date
divvy_df['START TIME'] = divvy_df['START TIME'].dt.time
divvy_df['STOP DATE'] = divvy_df['STOP TIME'].dt.date
divvy_df['STOP TIME'] = divvy_df['STOP TIME'].dt.time
divvy_df.head()

#Delete columns
divvy_df.drop('Unnamed: 0.2', axis=1, inplace=True)
divvy_df.drop('Unnamed: 0', axis=1, inplace=True)
divvy_df.drop('Unnamed: 0.1', axis=1, inplace=True)

# Organize columns in dataframe
divvy_df.columns
divvy_df = divvy_df[["TRIP ID", "BIKE ID", "START DATE", "START TIME", "time difference", "STOP DATE", "STOP TIME", "TRIP DURATION", "Year", "Month", "Day","Hour", "Day of Week", "FROM STATION ID", "TO STATION ID", "USER TYPE", "GENDER", "BIRTH YEAR", "AGE", "Age Group"]]
divvy_df.head(10)

#Export CSV dataframe
path = r'C:\Users\HP\Desktop\DIVVY DATA FULL\Preprocessing divvy 2019.csv'
divvy_df.to_csv(path)
# Import Dependencies
from matplotlib import pyplot as plt
import seaborn as sns
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
divvy_df = pd.read_csv('C:/Users/HP/Desktop/DIVVY DATA FULL/Preprocessing divvy 2019.csv')
divvy_df.shape

divvy_df.columns

#divvy_df.loc[divvy_df['time difference']==-56.36666666666667]
#cols = [813567,814409,814931,817201,818584,820755,821880,824658]
#divvy_df.dropna(divvy_df.index[cols], axis=1, inplace=True)

# Number of unique bikes in circulation
divvy_df['BIKE ID'].nunique()

divvy_df['Age Group'].unique()

divvy_df.iloc[['20-Nov'],['Age Group']]= "10-20"
divvy_df.loc[divvy_df['Age Group'] == "20-Nov", "Age Group"] = "10-20"



# Bike IDs with most activity
divvy_df['BIKE ID'].value_counts()

# Identify min / max duration of rides
max_duration = divvy_df['time difference'].max()
min_duration = divvy_df['time difference'].min()
mean = divvy_df['time difference'].mean()
median = divvy_df['time difference'].median()
mode = divvy_df['time difference'].mode()


# Print Summary Trip Duration Stats
print('Summary Trip Duration Statistics')
print(f'Max: {max_duration}')
print(f'Min: {min_duration}')
print(f'Mean: {mean}')
print(f'Median: {median}')
print(f'Mode: {mode}')

# Plot Trip Duration for Whole Dataset
plt.figure(figsize=(13,10))
Trip_Duration_All_data = plt.scatter(divvy_df['time difference'], divvy_df['BIKE ID'], color="violet", alpha = .3, edgecolors='violet')
plt.title("Trip Duration for Whole Dataset")
plt.xlabel("Trip Duration (Minutes)")
plt.ylabel("Bike ID")
#plt.savefig('Images/Trip_Duration_Scatter_All.png')
plt.show()

# c
clustered_duration = divvy_df.loc[divvy_df['time difference']<=100]
clustered_duration
clustered_duration.value_counts()

# Plot Trip Duration by Bike ID
plt.figure(figsize=(13,10))
plt.scatter(clustered_duration['time difference'], clustered_duration['BIKE ID'], color="deepskyblue", alpha = .3, edgecolors='deepskyblue')
plt.title("Trip Duration for Trips Less Than or Equal to 100 Minutes")
plt.xlabel("Trip Duration (Minutes)")
plt.ylabel("Bike ID")
#plt.savefig('Images/Trip_Duration_Scatter_Under_100.png')
plt.show()

popular_bikes = divvy_df['BIKE ID'].value_counts().head(20)
popular_bikes

# Rides for top 20 bikes
divvy_df['BIKE ID'] = divvy_df['BIKE ID'].astype(str)
divvy_df['BIKE ID'].dtypes
plt.figure(figsize=(13,7))
plt.bar(divvy_df['BIKE ID'].head(20), popular_bikes, color='deepskyblue')
plt.title("Number of Rides for The Top 20 Bikes")
plt.xlabel("Bike ID")
plt.ylabel("Number of Rides")
plt.grid(True, alpha=.5)
#plt.savefig('Images/Rides_per_Top_20_Bikes.png')


# Find 20 most used bike IDs
popular_bikes = divvy_df['BIKE ID'].value_counts().head(20)
popular_bikes

# Convert bike ID to string
divvy_df['BIKE ID'] = divvy_df['BIKE ID'].astype(str)
divvy_df['BIKE ID'].dtypes


# Identify the most popular starting stations
top_routes = divvy_df['FROM STATION ID'].value_counts()
total_trips_df = pd.DataFrame({
    'total trips': top_routes
})

# Reduce the results to any stations with trip greater than or equal to 10,000
total_trips_reduced = total_trips_df.loc[total_trips_df['total trips'] >= 10000]
total_trips_reduced


# Display a bar chart of the 7 most popular stations
total_trips_reduced.plot(kind='bar', color='deepskyblue', alpha=.5, align='center', figsize=(20,10))
plt.title('Most Popular Stations')
plt.xlabel('Stations')
plt.ylabel('Trips')
#plt.savefig('Images/Most_Popular_Stations.png')
plt.show()
plt.tight_layout()


# Create a dataframe shows the most popular ending station for popular starting stations
divvy_rides = {'from_station': divvy_df['FROM STATION ID'],
               'to_station': divvy_df['TO STATION ID']
              }

divvy_rides_df = pd.DataFrame(divvy_rides, columns=['from_station', 'to_station'])
dup_to_from = divvy_rides_df.pivot_table(index=['from_station', 'to_station'], aggfunc='size')

# Reconfigure dataframe to display data side by side
dup_to_from.columns = dup_to_from.droplevel(0)
dup_to_from.columns.name = None
dup_to_from_II = dup_to_from.reset_index()

# Rename dataframe columns
to_from_III = dup_to_from_II.rename(columns={'from_station': 'from_station_id', 'to_station':'to_station_id', 0:'rides_taken'})
to_from_III

# Remove rows where start and end station were identical
to_from_removed_dups = to_from_III[to_from_III['from_station_id'] != to_from_III['to_station_id']]

# Sort dataframe of start/end stations, sort, and identify 25 most popular routes
most_pop_rides = to_from_removed_dups.loc[to_from_removed_dups.groupby('from_station_id')['rides_taken'].idxmax()]
most_popular_routes = most_pop_rides.sort_values(ascending=False, by='rides_taken').reset_index(drop=True)
most_popular_reduced = most_popular_routes[0:25]
most_popular_reduced

# Convert FROM STATION ID and TO STATION ID to string
divvy_df['FROM STATION ID'] = divvy_df['FROM STATION ID'].astype(str)
divvy_df['FROM STATION ID'].dtypes
divvy_df['TO STATION ID'] = divvy_df['TO STATION ID'].astype(str)
divvy_df['TO STATION ID'].dtypes

# Create a bar chart of the 25 most popular routes
plt.figure(figsize=(10,8))
plt.bar(most_popular_reduced['from_station_id'], most_popular_reduced['rides_taken'], color='mediumslateblue', alpha=.5, align='center')
plt.xticks(most_popular_reduced['from_station_id'], rotation='vertical')
plt.title('25 Most Popular Divvy Routes (Origin)')
plt.xlabel('Divvy Locations')
plt.ylabel('Number of Rides')
#plt.savefig('Images/Most Popular Routes.png')
plt.show()
plt.tight_layout()

divvy_df.columns = divvy_df.columns.str.replace('usertype', 'USER TYPE')
divvy_df.columns

#Comparing Subscribers & Customers

# Find amount ot Subscribers and Customers
divvy_df['USER TYPE'].value_counts()

# Groupby usertype for ridership breakdown
usertype_df = divvy_df.groupby('USER TYPE')
usertype_df.count()

#Usertype Percentage
# Count number of trips for each usertype
count_number_usertype = divvy_df['TRIP ID'].nunique()


# Count number of each usertype
usertype_number = usertype_df['TRIP ID'].nunique()

# Percentage Usertype Calculation
percent_usertype =  round((usertype_number / count_number_usertype * 100),)

# Display usertype demographics
usertype_demographics_df = pd.DataFrame({'Total Count':usertype_number,
                                       'Percentage':percent_usertype})
usertype_demographics_df.sort_values('Total Count', ascending = False)


#Use by Gender

# Examine count of non-null values
divvy_df.dtypes
divvy_df.info()

# Find amount of Male and Female riders
divvy_df['GENDER'].value_counts()

# Group by gender
usertype_gender_df = divvy_df.groupby('GENDER')

# Count number of trips for each gender
count_number_gender = divvy_df['TRIP ID'].nunique()

# Count number of each gender
gender_type_number = usertype_gender_df['TRIP ID'].nunique()

# Calculate percentage for gender
percent_gender =  round((gender_type_number / count_number_gender * 100),2)

# Display gender demographics
gender_demographics_df = pd.DataFrame({'Total Count':gender_type_number,
                                       'Percentage':percent_gender})
gender_demographics_df.sort_values('Total Count', ascending = False)

# Total Divvy Riders based on Gender- PIE CHART
gender_data = divvy_df['GENDER'].value_counts()
gender_labels = ['Male','Female']
colours = ['skyblue', 'lightpink']
plt.figure(figsize=(10,8))
plt.pie(gender_data, labels= gender_labels, colors=colours, autopct="%1.1f%%", startangle=145)
plt.title("Total Divvy Riders based on Gender")
#plt.savefig('Images/Gender_Overall.png')

#Use by Age Group

# Count number of trips for each age group
count_number_age = divvy_df['TRIP ID'].nunique()

# Count number in each age group and display
usertype_age_df = divvy_df.groupby('Age Group')
age_type_number = usertype_age_df['TRIP ID'].nunique()
usertype_age_df.count()

# Calculate percentage for age
percent_age =  age_type_number / count_number_age * 100

# Make df of age demographics
age_demographics_df = pd.DataFrame({'Total Count':age_type_number,
                                       'Percentage of Age':percent_age})
age_demographics_df.sort_values('Age Group', ascending = True)

# Percentage Divvy Riders based on Age- Bar Chart
rainbow_colors = ["dodgerblue", "deepskyblue", "cornflowerblue", "royalblue", "steelblue", "mediumblue", "skyblue", "navy"]
plt.figure(figsize=(10,8))
percent_chart = percent_age.plot(kind = 'bar', color = rainbow_colors, rot = 20)
#plt.savefig('Images/Age_Overall.png')
plt.figure(figsize=(10,8))
percent_chart.set_ylabel("Percent")
percent_chart.set_xlabel("Age Group")
percent_chart.set_title("Percentage Divvy Riders Based on Age")

# Age seperated by usertype
usertype_age_df['USER TYPE'].value_counts()

# Total Divvy Riders based on Age, Separated by Usertype- Stacked Histogram
subscriber_age_totals = [12270,342425,287671,123787,87457,29511,1961,40]
customer_age_totals = [3688,34844,14128,5095,2828,512,33,7]
plotdata = pd.DataFrame({
    "Subscriber":subscriber_age_totals,
    "Customer":customer_age_totals
    },
    index = ['10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90']
    )
plotdata[["Subscriber", "Customer"]].plot(kind="bar", color=['deepskyblue','orchid'], stacked=True)
plt.title("Total Divvy Riders based on Age, Separated by Usertype")
plt.xlabel("Age Groups")
plt.ylabel("Amount of Riders")
#plt.savefig('Images/Age_Customers_and_Subscribers.png')



# Find amount of trips based on day of week
divvy_df['Day of Week'].value_counts()

# Groupby day of week for ridership breakdown
DayTrip_df = divvy_df.groupby('Day of Week')
DayTrip_df.count()


#Usertype Percentage
# Count number of trips for each day of week 
count_number_DayTrip = divvy_df['TRIP ID'].nunique()

print(divvy_df['USER TYPE'].unique())

# Count number of each day of week
DayTrip_number = DayTrip_df['TRIP ID'].nunique()

# Percentage Usertype Calculation
percent_DayTrip =  round((DayTrip_number / count_number_DayTrip * 100),)

# Display DayTrip demographics
DayTrip_demographics_df = pd.DataFrame({'Total Count':DayTrip_number,
                                       'Percentage':percent_DayTrip})
DayTrip_demographics_df.sort_values('Total Count', ascending = False)


navy_colors = ["slateblue", "darkslateblue", "indigo", "blueviolet", "plum", "mediumorchid", "orchid"]
plt.figure(figsize=(10,8))
percent_chart = percent_DayTrip.plot(kind = 'bar', color = navy_colors, rot = 20)
#plt.savefig('Images/Age_Overall.png')
plt.figure(figsize=(10,8))
percent_chart.set_ylabel("Percent")
percent_chart.set_xlabel("Days of Week")
percent_chart.set_title("Percentage Divvy Riders Based on Day of Week")

# Find amount of trips based on hour of day
divvy_df['Hour'].value_counts()

# Groupby day of week for ridership breakdown
HourTrip_df = divvy_df.groupby('Hour')
HourTrip_df.count()


#Usertype Percentage
# Count number of trips for each hour of day 
count_number_HourTrip = divvy_df['TRIP ID'].nunique()


# Count number of each hour of day
HourTrip_number = HourTrip_df['TRIP ID'].nunique()

# Percentage Hour of day Trip Calculation
percent_HourTrip =  round((HourTrip_number / count_number_HourTrip * 100),)

# Display HourTrip demographics
HourTrip_demographics_df = pd.DataFrame({'Total Count':HourTrip_number,
                                       'Percentage':percent_HourTrip})
HourTrip_demographics_df.sort_values('Total Count', ascending = False)

navy_colors = ["slateblue", "navy", "indigo"]
plt.figure(figsize=(10,8))
percent_chart = percent_HourTrip.plot(kind = 'bar', color = navy_colors, rot = 20)
#plt.savefig('Images/Age_Overall.png')
plt.figure(figsize=(10,8))
percent_chart.set_ylabel("Percent")
percent_chart.set_xlabel("Hour of Day")
percent_chart.set_title("Percentage Divvy Riders Based on Hour of Day")

#Comparing Subscribers & Customers

# Groupby usertype for ridership breakdown
usertype_df = divvy_df.groupby('USER TYPE')
usertype_df.count()

# Find amount ot Subscribers and Customers
divvy_df['USER TYPE'].value_counts()

# Find Usertype Percentage

# Count number of trips for each usertype
count_number_usertype = divvy_df['TRIP ID'].nunique()

# Count number of each usertype
usertype_number = usertype_df['TRIP ID'].nunique()

# Percentage Usertype Calculation
percent_usertype =  round((usertype_number / count_number_usertype * 100),)

# Display usertype demographics
usertype_demographics_df = pd.DataFrame({'Total Count':usertype_number,
                                       'Percentage':percent_usertype})
usertype_demographics_df.sort_values('Total Count', ascending = False)


usertype_data = divvy_df['USER TYPE'].value_counts()
usertype_labels = ['Subscriber','Customer']
colours = ['deepskyblue', 'violet']
plt.figure(figsize=(10,8))
plt.pie(usertype_data, labels= usertype_labels, colors=colours, autopct="%1.1f%%", startangle=145)
plt.title("Total Divvy Riders based on User type")
#plt.savefig('Images/Gender_Overall.png')

# Find breakdown of each gender for each usertype
usertype_gender_df['USER TYPE'].value_counts()

# Total Divvy Riders based on Gender and Usertype- Bar Graph
split_gender_data = usertype_gender_df['USER TYPE'].value_counts()
blue_colors = ["deepskyblue", "lightskyblue", "steelblue", "lightsteelblue"]
plt.figure(figsize=(10,8))
gender_chart = split_gender_data.plot(kind = 'bar', color = blue_colors, rot = 20)
gender_chart.set_ylabel("Amount of Riders")
gender_chart.set_xlabel("Gender, Usertype")
gender_chart.set_title("Total Divvy Riders based on Gender and Usertype")
#plt.savefig('Images/Gender_Customers_Only.png')
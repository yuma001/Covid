# To import csv and read it properly
import pandas as pd
 
df = pd.read_csv("Data/owid-covid-dat.csv")

# Explore the data
print(df.head())
print(df.info())

# Only want some columns from the data
country_over_time = df[['continent'
                    , 'location'
                    , 'date'
                    , 'new_cases'
                    , 'new_deaths'
                    , 'people_vaccinated'
                    , 'population']]

print(country_over_time.head())

country_total = df[['continent'
                    , 'location'
                    , 'date'
                    , 'total_cases'
                    , 'total_deaths'
                    , 'population']]

print(country_total.head())

# Want to get max cases so only one row for each country
country_max_cases = country_total.groupby('location').total_cases.max()
print(country_max_cases.head())


# To import csv and read it properly
import pandas as pd
 
df = pd.read_csv("Data/owid-covid-dat.csv")

# Explore the data
print(df.head())
print(df.info())

# Only want some columns from the data
# New cases/deaths
country_over_time = df[['continent'
                    , 'location'
                    , 'date'
                    , 'new_cases'
                    , 'new_deaths'
                    , 'population']]

print(country_over_time.head())

# Total cases/deaths
country_total = df[['continent'
                    , 'location'
                    , 'date'
                    , 'total_cases'
                    , 'total_deaths'
                    , 'population']]

print(country_total.head())


# Remove the continents as locations for new cases/deaths df
country_minus_continents_new = country_over_time[~country_over_time.continent.isnull()]
# Testing: print(country_minus_continents[country_minus_continents.location == 'Africa'])

# Create table with just new cases with NULLS removed
new_cases = country_over_time.drop('new_deaths', axis=1) # Dropping column as not needed. Axis=1 refers to columns. If was 0, then it would refer to rows.
new_cases_no_nulls = new_cases[~new_cases.new_cases.isnull()] # Remove nulls
print(new_cases_no_nulls.head())

# Create table with just new deaths with NULLS removed
new_deaths = country_over_time.drop('new_cases', axis=1) 
new_deaths_no_nulls = new_deaths[~new_deaths.new_deaths.isnull()] 
print(new_deaths_no_nulls.head())

# Remove the continents as locations for total cases/deaths df
country_minus_continents_total = country_total[~country_total.continent.isnull()]
# Testing: print(country_minus_continents[country_minus_continents.location == 'Africa'])

# Want to get max total cases so only one row for each country
total_cases_no_nulls = country_minus_continents_total[~country_minus_continents_total.total_cases.isnull()] 
max_total_cases_grouped = total_cases_no_nulls.loc[total_cases_no_nulls.groupby('location')['total_cases'].idxmax()].reset_index(drop=True) # Group by country
max_total_cases = max_total_cases_grouped.drop('total_deaths', axis=1) 
print(max_total_cases.head())

# Want to get max total deaths so only one row for each country
total_deaths_no_nulls = country_minus_continents_total[~country_minus_continents_total.total_deaths.isnull()] 
max_total_deaths_grouped = total_deaths_no_nulls.loc[total_deaths_no_nulls.groupby('location')['total_deaths'].idxmax()].reset_index(drop=True)
max_total_deaths = max_total_deaths_grouped.drop('total_cases', axis=1)
print(max_total_deaths.head())

# Since there is only one row for each country, joining the dfs
total_merged = max_total_cases.merge(max_total_deaths, left_on='location', right_on='location', suffixes=('_cases', '_deaths')) # Join the two total dfs
total_dropped_columns = total_merged.drop(['population_cases', 'continent_deaths'], axis=1)
total_dropped_columns.rename(columns = {'continent_cases':'continent', 'population_deaths':'population'}, inplace=True) # Renaming columns
print(total_dropped_columns.head())

# Write all df to csv 
new_cases_no_nulls.to_csv('Data/new_cases.csv')
new_deaths_no_nulls.to_csv('Data/new_deaths.csv')
total_dropped_columns.to_csv('Data/total_cases_deaths.csv')
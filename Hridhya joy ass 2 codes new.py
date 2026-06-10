# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:14:04 2023

@author: hridh
"""
#Importing the packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def world_bank_data_reading(filename):
    
    df = pd.read_csv(filename)

    # Transpose the dataframe to have years as columns and countries as rows
    df_transposed = df.melt(id_vars=['Country Name', 'Country Code', 'Series Code','Series Name'],
                                value_vars = df.columns[3:],
                                var_name = 'Year',
                                value_name = 'Value')

    # Pivot the transposed dataframe to have years as columns
    data_year = df_transposed.pivot_table(index = ['Country Name', 'Country Code', 'Series Code','Series Name'],
                                             columns = 'Year',
                                             values = 'Value',
                                             aggfunc = 'first').reset_index()

    # Pivot the transposed dataframe to have countries as columns
    data_country = df_transposed.pivot_table(index = ['Year', 'Series Code'],
                                               columns = ['Country Name', 'Country Code'],
                                               values = 'Value',
                                               aggfunc = 'first').reset_index()

    # Drop unnecessary columns and reset the index
    data_year.reset_index(drop=True, inplace = True)
    data_country.reset_index(drop=True, inplace = True)
    
    # Clean the transposed dataframe
    df_transposed.columns.name = None  
    df_transposed = df_transposed.rename_axis(None, axis=1)  

    return data_year, data_country, df_transposed




def main():
   
    filename = "climate_data.csv"
    data_year, data_country, df_transposed = world_bank_data_reading(filename)
    
    # Print the dataframe with years as columns
    print("\nDataframe with Years as Columns:")
    print(data_year.head())

    # Print the dataframe with countries as columns
    print("\nDataframe with Countries as Columns:")
    print(data_country.head())

    # Print the transposed and cleaned dataframe
    print("\nTransposed and Cleaned DataFrame:")
    print(df_transposed.head())
    
    # Perform statistical analysis on transposed_data
    print("\nSummary Statistics:")
    summary_stats = df_transposed.describe()
    print(summary_stats)

if __name__ == "__main__":
    main()
 
    
    
    
def save_and_read_transposed_data():
    filename = r"C:\Users\hridh\Desktop\assignment 2\climate_data.csv"
    _, _, df_transposed = world_bank_data_reading(filename)

    # Save transposed_data to a CSV file
    df_transposed.to_csv("df_transposed.csv", index = False)
    print("Transposed data saved to 'df_transposed.csv'.")

    # Read the saved CSV file back to a dataframe
    loading_dataset = pd.read_csv("df_transposed.csv")
    print("Transposed data:")
    print(loading_dataset.head())

if __name__ == "__main__":
    save_and_read_transposed_data()
    
    
wb_data=pd.read_csv('df_transposed.csv')
wb_data.head()


wb_data.info()


wb_data['Value'] = wb_data['Value'].replace('[^\d.]', '', regex=True)
wb_data['Value'] = pd.to_numeric(wb_data['Value'], errors='coerce')
wb_data = wb_data.dropna(subset=['Value'])
wb_data.reset_index(drop=True, inplace=True)
wb_data.tail()


wb_data.isnull().sum()


wb_data.describe()


print("Basic Statistics:")
print(wb_data['Value'].describe())

# Display mean of the 'Value' column
mean_value = wb_data['Value'].mean()
print(f"\nMean of 'Value': {mean_value}")

# Display median of the 'Value' column
median_value = wb_data['Value'].median()
print(f"Median of 'Value': {median_value}")

# Display standard deviation of the 'Value' column
std_dev_value = wb_data['Value'].std()
print(f"Standard Deviation of 'Value': {std_dev_value}")



wb_data.head()



year_data = wb_data.pivot_table(index=['Country Name', 'Country Code', 'Series Code','Series Name'],
                          columns='Year', values='Value').reset_index()

year_data.head()


plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Value', hue='Country Name', data=wb_data[wb_data['Series Code'] == 'EG.FEC.RNEW.ZS'])
plt.title('Renewable energy consumption Over the Years for Different Countries')
plt.xlabel('Year')
plt.ylabel('Renewable energy consumption')
plt.legend(title='Country')
plt.show()



recent_years = wb_data['Year'].max()
gdp_growth_data_recent = wb_data[(wb_data['Series Name'] == 'GDP growth (annual %)') & (wb_data['Year'] >= recent_years - 4)]

# Plot the bar chart of GDP growth of Recent 5 Years for Different Countries
plt.figure(figsize=(12, 8))
sns.barplot(x='Year', y='Value', hue='Country Name', data=gdp_growth_data_recent)
plt.title('GDP Growth (Annual %) Over the Most Recent 5 Years for Different Countries')
plt.xlabel('Year')
plt.ylabel('GDP Growth (Annual %)')
plt.legend(title='Country', loc='upper left', bbox_to_anchor=(1, 1))
plt.show()



electric_power_data = wb_data[wb_data['Series Name'] == 'Electric power consumption (kWh per capita)']

# Plot the line chart for Electric Power Consumption for Different Countries
plt.figure(figsize=(12, 8))
sns.lineplot(x='Year', y='Value', hue='Country Name', data=electric_power_data)
plt.title('Electric Power Consumption Over the Years for Different Countries')
plt.xlabel('Year')
plt.ylabel('Electric Power Consumption (kWh per capita)')
plt.legend(title='Country', loc='upper left', bbox_to_anchor=(1, 1))
plt.show()


'''***CORRELATION ANALYSIS***'''

correlation_data = wb_data[['Country Name', 'Series Name', 'Year', 'Value']]

# Pivot the data to create a matrix with years as rows and series names as columns
pivot_data = correlation_data.pivot_table(index=['Country Name', 'Year'], columns='Series Name', values='Value', aggfunc='first')

# Calculate the correlation matrix
correlation_matrix = pivot_data.corr()

# Create the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap for Different Series Names')
plt.show()

print(correlation_matrix)



# Filter data for the specific series
filtered_data = wb_data[wb_data['Series Name'] == 'Fossil fuel energy consumption (% of total)']

# Create a pie chart Fossil fuel energy consumption distribution by country
plt.figure(figsize=(15, 10))
plt.pie(filtered_data.groupby('Country Name')['Value'].sum(), labels=filtered_data['Country Name'].unique(), autopct='%1.1f%%', startangle=140)
plt.title('Fossil fuel energy consumption distribution by country')
plt.show()

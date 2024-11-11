# dashboard/dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv("main_data.csv") 

# Convert 'datetime' column to datetime type if not already done
data['datetime'] = pd.to_datetime(data['datetime'])

# Set up the Streamlit app
st.title("Air Quality Analysis Dashboard")
st.sidebar.header("Filter Options")

# Date range filter
date_range = st.sidebar.slider("Select Date Range:", 
                               min_value=data['datetime'].min().date(), 
                               max_value=data['datetime'].max().date(), 
                               value=(data['datetime'].min().date(), data['datetime'].max().date()))

# Filter by location
location = st.sidebar.selectbox("Select Location:", options=data['station'].unique())
filtered_data = data[(data['datetime'].dt.date.between(date_range[0], date_range[1])) & 
                     (data['station'] == location)]

# Display summary statistics
st.header(f"Air Quality Summary for {location}")
st.write(filtered_data.describe())

# Plot PM2.5 and PM10 trends over time
st.subheader("PM2.5 and PM10 Concentration Over Time")
fig, ax = plt.subplots(2, 1, figsize=(10, 8))

# PM2.5 Plot
ax[0].plot(filtered_data['datetime'], filtered_data['PM2.5'], label="PM2.5", color='blue')
ax[0].set_xlabel("Date")
ax[0].set_ylabel("PM2.5 Concentration")
ax[0].set_title("PM2.5 Concentration Over Time")

# PM10 Plot
ax[1].plot(filtered_data['datetime'], filtered_data['PM10'], label="PM10", color='red')
ax[1].set_xlabel("Date")
ax[1].set_ylabel("PM10 Concentration")
ax[1].set_title("PM10 Concentration Over Time")

plt.tight_layout()
st.pyplot(fig)

# Visualisasi Tren Polutan Lainnya
st.subheader("Trends of Other Pollutants Over Time")
fig, ax = plt.subplots(2, 2, figsize=(12, 10))

pollutants = ['SO2', 'NO2', 'CO', 'O3']
colors = ['purple', 'orange', 'green', 'brown']
for i, pollutant in enumerate(pollutants):
    row, col = i // 2, i % 2
    ax[row, col].plot(filtered_data['datetime'], filtered_data[pollutant], color=colors[i])
    ax[row, col].set_title(f"{pollutant} Concentration Over Time")
    ax[row, col].set_xlabel("Date")
    ax[row, col].set_ylabel(f"{pollutant} Concentration")

plt.tight_layout()
st.pyplot(fig)

# Monthly Trend of PM2.5 and PM10 - Ensure only numeric columns are included
monthly_data = filtered_data.set_index('datetime').select_dtypes(include='number').resample('M').mean()

st.subheader("Monthly Average Concentration of PM2.5 and PM10")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_data.index, monthly_data['PM2.5'], label="PM2.5", color='blue')
ax.plot(monthly_data.index, monthly_data['PM10'], label="PM10", color='red')
ax.set_xlabel("Month")
ax.set_ylabel("Monthly Average Concentration")
ax.set_title("Monthly Average Concentration of PM2.5 and PM10")
ax.legend()
st.pyplot(fig)

# Distribution of PM2.5 Concentrations
st.subheader("Distribution of PM2.5 Concentrations")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_data['PM2.5'], bins=30, kde=True, color='blue', ax=ax)
ax.set_title("Distribution of PM2.5 Concentrations")
ax.set_xlabel("PM2.5 Concentration")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Scatterplot for PM2.5 vs Temperature
st.subheader("PM2.5 vs Temperature")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x='TEMP', y='PM2.5', data=filtered_data, ax=ax)
ax.set_title("Scatterplot of PM2.5 vs Temperature")
ax.set_xlabel("Temperature")
ax.set_ylabel("PM2.5 Concentration")
st.pyplot(fig)

# Correlation Heatmap
st.subheader("Correlation Matrix")
correlation_matrix = filtered_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
st.pyplot(fig)


# Plot PM2.5 and PM10 trends over time with monthly aggregation
st.subheader("Monthly Trend of PM2.5 and PM10 Across Locations")
monthly_data = filtered_data.set_index('datetime').resample('M').mean(numeric_only=True).reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='datetime', y='PM2.5', data=monthly_data, label='PM2.5', ax=ax)
sns.lineplot(x='datetime', y='PM10', data=monthly_data, label='PM10', ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Concentration")
ax.set_title("Monthly Average Concentration of PM2.5 and PM10")
st.pyplot(fig)

# Dominant Pollutant by Location and Weather Influence
st.subheader("Dominant Pollutant and Weather Influence by Location")
dominant_pollutant = filtered_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().idxmax()
st.write(f"The dominant pollutant at {location} is: {dominant_pollutant}")

# Show correlation with weather features
st.subheader("Correlation Between Pollutants and Weather")
correlation_matrix = filtered_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
st.pyplot(fig)

# Scatter plot for each pollutant and weather variable
st.subheader("Scatter Plots: Pollutants vs. Weather Variables")
for feature in ['TEMP', 'DEWP', 'WSPM']:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=feature, y='PM2.5', data=filtered_data, ax=ax)
    ax.set_title(f"PM2.5 vs {feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel("PM2.5 Concentration")
    st.pyplot(fig)

# Pollution Level by Time of Day
st.subheader("Pollution Level by Time of Day")
filtered_data['Time of Day'] = pd.cut(filtered_data['datetime'].dt.hour, 
                                      bins=[0, 6, 12, 18, 24], 
                                      labels=['Night', 'Morning', 'Afternoon', 'Evening'],
                                      right=False)
time_of_day_avg = filtered_data.groupby('Time of Day')[['PM2.5', 'PM10']].mean().reset_index()
fig, ax = plt.subplots()
time_of_day_avg.plot(x='Time of Day', y=['PM2.5', 'PM10'], kind='bar', ax=ax)
ax.set_ylabel("Average Concentration")
ax.set_title("Pollution Level by Time of Day")
st.pyplot(fig)


# 5. Effect of Rain on Pollutant Levels
st.subheader("Effect of Rain on PM2.5 Levels")
rain_data = filtered_data.groupby(filtered_data['RAIN'] > 0)['PM2.5'].mean()
rain_labels = ['No Rain', 'Rain']
fig, ax = plt.subplots()
ax.bar(rain_labels, rain_data, color=['skyblue', 'slateblue'])
ax.set_ylabel("Average PM2.5 Concentration")
ax.set_title("Effect of Rain on PM2.5 Concentration")
st.pyplot(fig)

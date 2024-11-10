# Air Quality Analysis Project

## Table of Contents
- [Data Source](#data-source)
- [Libraries Used](#libraries-used)
- [Key Insights](#key-insights)
- [How to Run the Dashboard](#how-to-run-the-dashboard)

## Data Source
The dataset used in this project includes air quality measurements from 12 stations, with a focus on PM2.5, PM10, and other environmental factors like temperature, dew point, humidity, and wind speed.

## Libraries Used
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- NumPy
- SciPy

## Key Insights
- Monthly trends in PM2.5 and PM10 levels, highlighting seasonal variations.
- Comparison of dominant pollutants across locations and their correlation with weather conditions.
- Insights into how temperature, humidity, and wind speed impact pollution levels.
- Analysis of pollution variations by time of day.
- Examination of rainfall effects on pollutant concentration levels.

## How to Run the Dashboard

To run the Air Quality Analysis Dashboard, follow these steps:

### Setup Environment

1. **Create and Activate a Python Environment**:
   - If using Conda (ensure [Conda](https://docs.conda.io/en/latest/) is installed):
     ```bash
     conda create --name airquality-ds python=3.9
     conda activate airquality-ds
     ```
   - If using venv (standard Python environment tool):
     ```bash
     python -m venv airquality-ds
     source airquality-ds/bin/activate  # On Windows use `airquality-ds\Scripts\activate`
     ```

2. **Install Required Packages**:
   - Install packages using:
     ```bash
     pip install pandas numpy scipy matplotlib seaborn streamlit
     ```
   - Or install all dependencies using:
     ```bash
     pip install -r requirements.txt
     ```

### Run the Streamlit App

1. **Navigate to the Project Directory** where `dashboard.py` is located in the `dashboard` folder.

2. **Run the Streamlit App**:
    ```bash
    streamlit run dashboard/dashboard.py
    ```

### Additional Files

- `main_data.csv` contains the combined dataset used in this analysis.
- A detailed Python notebook (`notebook.ipynb`) includes data analysis and visualizations for in-depth understanding.

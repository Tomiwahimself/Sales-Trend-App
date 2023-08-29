import pandas as pd

def load_data(filename):
    return pd.read_csv(filename)
def preprocess_data(data):
    data['Date'] = pd.to_datetime(data['Date'])  # Converting 'Date' column to datetime
    return data

if __name__ == "__main__":
    data = load_data('/Users/tomiwa/Documents/Portfolio/Sales_Trend Project/sales_data.csv')  
    preprocessed_data = preprocess_data(data)  # Preprocessing data using the function from data_preprocessing.py
    
    # Seasonal Analysis
    monthly_sales = preprocessed_data.resample('M', on='Date')['Weekly_Sales'].sum()
    print("Monthly Sales:", monthly_sales)

    # Holiday Impact Analysis
    holiday_sales = preprocessed_data.groupby('Holiday_Flag')['Weekly_Sales'].mean()
    print("Average Sales during Holidays:\n", holiday_sales)

    # Correlation Analysis
    correlation_matrix = preprocessed_data[['Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']].corr()
    print("Correlation Matrix:\n", correlation_matrix)

    # Sales Trend over Years
    yearly_sales = preprocessed_data.resample('Y', on='Date')['Weekly_Sales'].sum()
    print("Yearly Sales Trend:\n", yearly_sales)

    # Sales Growth Rate
    preprocessed_data['Sales_Growth'] = preprocessed_data['Weekly_Sales'].pct_change()
    print("Sales Growth Rate:\n", preprocessed_data['Sales_Growth'])

    # Weekday vs. Weekend Analysis
    preprocessed_data['Weekday'] = preprocessed_data['Date'].dt.weekday
    weekday_sales = preprocessed_data.groupby('Weekday')['Weekly_Sales'].mean()
    print("Weekday Sales:\n", weekday_sales)
   
    # Unemployment Impact Analysis
    unemployment_sales = preprocessed_data.groupby('Unemployment')['Weekly_Sales'].mean()
    print("Average Sales by Unemployment Rate:\n", unemployment_sales)

    # Lagged Analysis (assuming a sorted DataFrame by 'Date')
    preprocessed_data['Weekly_Sales_Lagged'] = preprocessed_data['Weekly_Sales'].shift(1)
    print("Lagged Sales:\n", preprocessed_data['Weekly_Sales_Lagged'])

    # Rolling Mean (e.g., 7-day rolling mean)
    rolling_mean = preprocessed_data['Weekly_Sales'].rolling(window=7).mean()
    print("7-day Rolling Mean:\n", rolling_mean)

#Other Analysis are on the Streamlit app 

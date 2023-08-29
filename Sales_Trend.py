import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Loading preprocessed data
data = pd.read_csv('/Users/tomiwa/Documents/Portfolio/Sales_Trend Project/sales_data.csv')

# Converting 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

# Titling and Description
st.title('Sales Trend Analysis App')
st.write('Explore sales trends, patterns, and predictions.')

# Displaying the dataset
st.subheader('Complete Dataset')
st.dataframe(data)

# Sidebar for user input
st.sidebar.header('Change Output')
selected_store = st.sidebar.selectbox('Select Store', data['Store'].unique())
selected_date = st.sidebar.date_input('Select Date')

# Displaying patterns, trends, and predictions
if selected_store:
    st.sidebar.subheader('View Sections')
    selected_section = st.sidebar.selectbox('Select Section', ['Patterns', 'Trends', 'Predictions'])

    # Filtering data based on user input
    filtered_data = data[data['Store'] == selected_store]
    train_data = filtered_data.iloc[:len(filtered_data) - 12]  # Defining train_data for Patterns and Predictions


    if selected_section == 'Patterns':
        st.subheader('Sales Patterns')

        # Quarterly sales trend for each store in a tabular form
        quarterly_trends = filtered_data.groupby(['Store', filtered_data['Date'].dt.to_period('Q')])['Weekly_Sales'].sum().unstack()
        st.write('Quarterly Sales Trend for Each Store')
        st.dataframe(quarterly_trends)

        # Average sales yearly for the selected store
        avg_sales_by_year = filtered_data.groupby(filtered_data['Date'].dt.year)['Weekly_Sales'].mean()
        st.subheader(f'Average Sales by Year for Store {selected_store}')
        st.bar_chart(avg_sales_by_year)

        

    elif selected_section == 'Trends':
        st.subheader('Sales Trends')

        # Insight: Identify overall sales trends over time
        overall_sales_trend = filtered_data.groupby(filtered_data['Date'].dt.year)['Weekly_Sales'].sum().diff().mean()
        st.write('Average Sales Trend over Years:', overall_sales_trend)

        # Visualization: Line plot showing sales trend over the years
        st.subheader('Sales Trend over the Years')
        trend_data = filtered_data.groupby(filtered_data['Date'].dt.year)['Weekly_Sales'].sum()
        st.line_chart(trend_data)
        

       

    elif selected_section == 'Predictions':
        st.subheader('Sales Predictions')
        # Split data into training and testing sets
        train_data = filtered_data.iloc[:len(filtered_data) - 12]
        test_data = filtered_data.iloc[len(filtered_data) - 12:]

    # Fit ARIMA model
        with st.spinner("Running ARIMA model..."):
            model = auto_arima(train_data['Weekly_Sales'], seasonal=True, m=12)

        # To make predictions
        predictions = model.predict(n_periods=len(test_data))

        # Calculating mean squared error
        mse = mean_squared_error(test_data['Weekly_Sales'], predictions)

        # Calculating other metrics
        rmse = mean_squared_error(test_data['Weekly_Sales'], predictions, squared=False)  # Root Mean Squared Error
        mae = mean_absolute_error(test_data['Weekly_Sales'], predictions)  # Mean Absolute Error

        # Determining accuracy category
        accuracy_category = ""
        if rmse < 100000:  
            accuracy_category = "Highly Accurate"
        elif rmse < 500000:
            accuracy_category = "Fairly Accurate"
        else:
            accuracy_category = "Not Accurate"

        # Displaying results
        st.write('ARIMA Model Results:')
        st.write('Predicted Sales:', predictions)
        st.write('Actual Sales:', test_data['Weekly_Sales'])
        st.write('Mean Squared Error:', mse)
        st.write('Root Mean Squared Error:', rmse)
        st.write('Mean Absolute Error:', mae)
        st.write('Accuracy Category:', accuracy_category)

    # Conclusion
    st.write('This Streamlit app provides an interactive way to explore sales trends, patterns, and predictions.')

# Footer
st.sidebar.write('Created by Emmanuel Isaiah')

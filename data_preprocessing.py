import pandas as pd

def preprocess_data(data):
    # Handling Missing Values
    data.fillna(0, inplace=True)  # Filling missing values with zeros

    # Data Type Conversion
    data['Date'] = pd.to_datetime(data['Date'])  # Replacing 'date_column' with the actual column name


    return data

# Loading the data
filename = '/Users/tomiwa/Documents/Portfolio/Sales_Trend Project/sales_data.csv'  
data = pd.read_csv(filename)

# Preprocessing the data
preprocessed_data = preprocess_data(data)

# Displaying info about preprocessed data
print(preprocessed_data.info())

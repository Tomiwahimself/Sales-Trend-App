import pandas as pd

def load_data(filename):
    return pd.read_csv('/Users/tomiwa/Documents/Portfolio/Sales_Trend Project/sales_data.csv')

# This code block will only run when you execute this script directly
if __name__ == "__main__":
    data = load_data('/Users/tomiwa/Documents/Portfolio/Sales_Trend Project/sales_data.csv')  
    print(data.info())

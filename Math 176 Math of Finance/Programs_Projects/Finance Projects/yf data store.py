import yfinance as yf
import pandas as pd
import numpy as np
import os

def OHLCV (list_tickers, start, end, interval):
    ohlv = {}
    for t in list_tickers:
        ohlv[t] = yf.download(t, start= start, end= end, interval= interval)

    return ohlv


def download_to_csv(dataframe, name: str) -> None:
    try:
        # Check if the input is a pandas DataFrame
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("The provided input is not a pandas DataFrame.")
        
        # Construct the full file path
        name = name + '.csv'
        directory = r"C:\Users\thoma\Desktop\Data\Finance"
        file_path = os.path.join(directory, name)
        
        # Save the dataframe to a CSV file
        dataframe.to_csv(file_path, index=False)

        print(f"DataFrame saved to {file_path}")

    except TypeError as e:
        print(f"Type error: {str(e)}")
    except PermissionError:
        print(f"Permission denied: Unable to write to {file_path}. Please check your permissions.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


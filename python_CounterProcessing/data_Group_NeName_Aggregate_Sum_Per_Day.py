import pandas as pd
import os

# File path
# file_path = r"D:\RawData\Others_Traffic_Test\ExportPerformanceQueryResult__20250320_200421_HOST45.csv"  # Path to your file
file_path = r"D:\RawData\Others_Traffic_Test\ExportPerformanceQueryResult__20250320_200421_HOST45.csv"  # Path to your file


try:
    

    # Read the file without specifying headers initially (raw load)
    raw_data = pd.read_csv(file_path, header=None)  # Load all rows and columns
    
    # Find the row index where the first column contains "Start Time"
    header_row_index = None
    for i, row in raw_data.iterrows():
        if row.iloc[0] == 'Start Time':  # Check if the first column matches "Start Time" (including quotes)
            header_row_index = i
            print("Detected header row number:" + str(header_row_index))
            break
    
    if header_row_index is not None:
        # Reload the file using the detected row as the header
        #df = pd.read_csv(file_path, header=header_row_index)
    
        # Load the CSV file, specifying that values may be quoted to handle extra commas
        df = pd.read_csv(file_path, header=header_row_index, quotechar='"', skipinitialspace=True)
    
        # Store column names in an array
        column_names = df.columns.tolist()
    
        # Print column names and their count
        print("Detected Table Headers:")
        print(column_names)
        print(f"Number of Columns: {len(column_names)}")
    
        # Display the first few rows of the DataFrame
        print("Here are the first few rows of the DataFrame:")
        print(df.head())
    else:
        print("The header row with '\"Start Time\"' was not found in the file.")
    
except FileNotFoundError:
    print(f"File not found: {file_path}")
except pd.errors.ParserError as e:
    print(f"Parser error: {e}")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

import pandas as pd
import os
from glob import glob

# Function to process a single file
def process_file(file_path):
    # Determine the file extension
    ext = os.path.splitext(file_path)[1].lower()
    
    # Read the file based on its type, setting low_memory=False to avoid DtypeWarning
    if ext == '.csv':
        df = pd.read_csv(file_path, skiprows=7, low_memory=False)
    elif ext in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path, skiprows=7)
    else:
        print(f"Unsupported file type: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame for unsupported files

    # Convert the datetime column (#1) to a datetime object
    df['Datetime'] = pd.to_datetime(df.iloc[:, 0], format='%m/%d/%Y %H:%M:%S')

    # Add a "Day" column (not required for the grouping by NE Name)
    df['Day'] = df['Datetime'].dt.date

    # Select only the columns we are interested in (NE Name and columns 5-11)
    selected_columns = [2] + list(range(4, 11))  # NE Name is column 3 (0-based)
    df = df.iloc[:, selected_columns]

    # Ensure numeric columns are indeed numeric for aggregation
    numeric_columns = df.columns[1:]  # Columns from index 1 onwards are numeric
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')  # Convert non-numeric values to NaN

    return df

# Function to process all supported files in a folder
def process_folder(folder_path, output_path):
    # List all supported files in the folder
    file_list = glob(os.path.join(folder_path, '*.csv')) + \
                glob(os.path.join(folder_path, '*.xls')) + \
                glob(os.path.join(folder_path, '*.xlsx'))
    
    if not file_list:
        print(f"No supported files found in folder: {folder_path}")
        return pd.DataFrame(), None, None  # Return an empty DataFrame if no files found

    processed_dfs = []
    date_values = []  # To store all datetime values

    for file_path in file_list:
        df = process_file(file_path)
        if not df.empty:
            processed_dfs.append(df)
            date_values.extend(pd.to_datetime(df.index))  # Extend datetime values from the Datetime column
    
    # Combine all processed dataframes
    combined_df = pd.concat(processed_dfs, ignore_index=True)
    
    # First and last dates in the input data
    first_date = min(date_values).date() if date_values else None
    last_date = max(date_values).date() if date_values else None
    
    # Group by NE Name and sum up the numeric columns
    grouped_by_ne_name = combined_df.groupby(combined_df.columns[0]).sum().reset_index()

    # Save the grouped table as a CSV file
    os.makedirs(output_path, exist_ok=True)  # Create the output folder if it doesn't exist
    output_file = os.path.join(output_path, 'outputGrouped_NEName_Aggregated_Total.csv')
    grouped_by_ne_name.to_csv(output_file, index=False)
    print(f"Grouped table by NE Name saved to: {output_file}")
    print(f"First Date: {first_date}, Last Date: {last_date}")

    return grouped_by_ne_name, first_date, last_date

# Specify the input and output folder paths
input_folder_path = r'D:\RawData\Others_Traffic'
output_folder_path = r'D:\RawData\procesing_Output'

# Process and save the grouped table, and print first and last dates
final_table, first_date, last_date = process_folder(input_folder_path, output_folder_path)

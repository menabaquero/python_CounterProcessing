import pandas as pd

# File path
file_path = r"D:\RawData\Others_Traffic_Test\ExportPerformanceQueryResult__20250320_200421_HOST45.csv"

try:
    # Step 1: Open the file and preprocess it
    with open(file_path, "r") as infile:
        lines = infile.readlines()  # Read all lines into a list

    # Step 2: Identify the line containing "Start Time"
    start_index = None
    for i, line in enumerate(lines):
        if '"Start Time"' in line:  # Look for the header row
            start_index = i
            break

    if start_index is None:
        print("The header row containing '\"Start Time\"' was not found in the file.")
    else:
        # Step 3: Overwrite the original file starting from the header row
        with open(file_path, "w") as outfile:
            outfile.writelines(lines[start_index:])  # Write from the header row onwards

        print(f"Metadata removed. Cleaned file saved with the same original file name: {file_path}")

        # Step 4: Load the cleaned file into pandas
        df = pd.read_csv(file_path, quotechar='"', sep=',', skipinitialspace=True)

        # Step 5: Print column names and their count
        column_names = df.columns.tolist()
        print("Detected Table Headers:")
        print(column_names)
        print(f"Number of Columns: {len(column_names)}")

        # Display the first few rows of the DataFrame
        print("Here are the first few rows of the DataFrame:")
        print(df.head())

except FileNotFoundError:
    print(f"File not found: {file_path}")
except pd.errors.ParserError as e:
    print(f"Parser error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

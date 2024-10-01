import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from pyproj import Transformer

# Set Pandas to display floating-point numbers in a more familiar format
pd.set_option('display.float_format', '{:.2f}'.format)

# Function to process each sensor of 5 coil system IVS files. Exproted from 'multi_sensor_data_processor.py' tool 
def EM61_5coil_ivs_file():
    # Prompt the user to enter the file path
    filename = input("Please enter the full path of the file: ")
    print('\n')

    try:
        # Open the file, read the first line (header), and remove the '/' if it exists
        with open(filename, 'r') as file:
            first_line = file.readline().strip()  # Read the first line (header)
            if first_line.startswith('/'):
                first_line = first_line[1:] 

        # Attempt to read the file using Pandas
        df = pd.read_table(filename, sep=r"\s+", header=0, skiprows=[0], names=first_line.split())
        # If successful, display the first few rows
        print("File loaded successfully! \n")

    except Exception as e:
        # If there is any error, print an error message
        print(f"Error: Unable to read the file. {e}")

    '''CLEANING AND FIXING FORMAT'''

    # Checking if 'DATE' and 'TIME' columns exist to proceed
    if 'DATE' in df.columns and 'TIME' in df.columns:
        df['DATETIME'] = df['DATE'] + ' ' + df['TIME']
        df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%m/%d/%y %H:%M:%S.%f')
    else:
        print("Error: 'DATE' and/or 'TIME' columns not found.")
        
    # Replacing empty spaces for NaN values
    df = df.replace(r'^\s*$', np.nan, regex=True)

    # Printing first lines of the data
    printOp = input("Enter 'Y' if you want to see the header of the data: \n").lower()

    if printOp == "y":
        print(df.head())
        print('\n')

    '''COORDINATE TRANSFORMATION'''

    # Assuming the first two columns are the coordinates (e.g., Easting and Northing)
    x_coords = df.iloc[:, 0]  # First column
    y_coords = df.iloc[:, 1]  # Second column

    # Define the source and target coordinate systems (you can change EPSG codes as needed)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32612", always_xy=True)  # WGS84 to UTM Zone 12N

    # Apply transformation to each pair of coordinates
    transformed_coords = [transformer.transform(x, y) for x, y in zip(x_coords, y_coords)]

    # Split transformed coordinates into X and Y and add them as new columns
    df['X'], df['Y'] = zip(*transformed_coords)

    print("Coordinate transformation completed! New 'X' and 'Y' columns added.\n")
    print(f"Transformation: {transformer} \n")

    '''CALCULATIONS'''
    # Calculate rolling statistic (median) without window shrinking
    df['CH_1_med'] = df['CH_1'].rolling(window=301, min_periods=1, center=True).median()
    df['CH_2_med'] = df['CH_2'].rolling(window=301, min_periods=1, center=True).median()
    df['CH_3_med'] = df['CH_3'].rolling(window=301, min_periods=1, center=True).median()
    df['CH_4_med'] = df['CH_4'].rolling(window=301, min_periods=1, center=True).median()
    
    # Calculate demedian. CH1_1_demed = CH_1 - CH_1_med
    df['CH_1_demed'] = df['CH_1'] - df['CH_1_med']
    df['CH_2_demed'] = df['CH_2'] - df['CH_2_med']
    df['CH_3_demed'] = df['CH_3'] - df['CH_3_med']
    df['CH_4_demed'] = df['CH_4'] - df['CH_4_med']

    print(df[['CH_1_med','CH_2_med','CH_3_med','CH_4_med']])

    '''PEAKS FINDING'''

    # Find peak indexes
    peaks_idx,_ = find_peaks(df['CH_1'],prominence=100)
    # Store peaks
    peaks = df.iloc[peaks_idx]
    # Reset rows index
    peaks.reset_index(drop=True, inplace=True)

    #If there is no peaks it goes back to the menu. For SSR files
    if peaks.empty:
        print('No peaks detected. Exiting to the menu...\n')
        plt.figure(figsize=(10, 6))
        plt.plot(df['DATETIME'],df['CH_1'],c='b')
        plt.title('CH_1 Data')
        plt.xticks(rotation=45)
        plt.show()
        return False

    '''PLOTTING'''

    plotResponse = input("Enter 'Y' if you want to plot the data: \n").lower()

    if plotResponse == 'y':
        print("Getting the plot... \n")

        plt.figure(figsize=(10, 6))
        plt.plot(df['DATETIME'],df['CH_1'],c='b')
        plt.plot(peaks['DATETIME'],peaks['CH_1'],'o',c='r')
        plt.title('IVS Plot')
        plt.xticks(rotation=45)
        plt.show()
    else:   print("Closing the program")

    # Printing peaks
    printOp1 = input("Enter 'Y' if you want to see the peaks of the signal: \n").lower()
    if printOp1 == "y":
        columns_to_print =  ['X', 'Y', 'CH_1', 'CH_1_med', 'TIME']
        print(peaks[columns_to_print])
        print('\n')

     # Ask if the user wants to work on another file
    continue_choice = input("Would you like to process another sensor file or go to the menu? (Y/N): \n").lower()
    
    if continue_choice == 'y':
        return True
    else:
        print("Exiting to the menu...\n")
        return False

# Function to process EM61 regular IVS files. Imported directly from EM61 and converted to .xyz
def EM61_ivs_file():
    # Prompt the user to enter the file path
    filename = input("Please enter the full path of the file: ")
    print('\n')

    columns = ['EAST', 'NORTH', 'STD-4-1', 'STD-4-2',
               'STD-4-3', 'STD-4-4', 'GPS Correction', 'TIME']

    try:
        # Attempt to read the file using Pandas
        df = pd.read_table(filename, sep=r"\s+",skiprows=2, names=columns, engine='python')
        # If successful, display the first few rows
        print("File loaded successfully! \n")

    except Exception as e:
        # If there is any error, print an error message
        print(f"Error: Unable to read the file. {e}")

     # Printing first lines of the data
    printOp = input("Enter 'Y' if you want to see the header of the data: \n").lower()

    if printOp == "y":
        print(df.head())
        print('\n')

    '''CLEANING AND FIXING FORMAT'''
    # Convert the TIME column to timestamp format
    df['TIME'] = pd.to_datetime(df['TIME'], format='%H:%M:%S.%f').dt.time   
    try:
        df['DATETIME'] = pd.to_datetime(df['TIME'], format='%H:%M:%S.%f', errors='coerce')
    except ValueError:
        df['DATETIME'] = pd.to_datetime(df['TIME'], format='%H:%M:%S', errors='coerce') 

    # Replacing empty spaces for NaN values
    df = df.replace(r'^\s*$', np.nan, regex=True)
    
    '''COORDINATE TRANSFORMATION'''

    # Assuming the first two columns are the coordinates (e.g., Easting and Northing)
    x_coords = df.iloc[:, 0]  # First column
    y_coords = df.iloc[:, 1]  # Second column

    # Define the source and target coordinate systems (you can change EPSG codes as needed)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32612", always_xy=True)  # WGS84 to UTM Zone 12N

    # Apply transformation to each pair of coordinates
    transformed_coords = [transformer.transform(x, y) for x, y in zip(x_coords, y_coords)]

    # Split transformed coordinates into X and Y and add them as new columns
    df['X'], df['Y'] = zip(*transformed_coords)

    print("Coordinate transformation completed! New 'X' and 'Y' columns added.\n")
    print(f"Transformation: {transformer} \n")

    '''CALCULATIONS'''
    '''Modify this section: Following the QC process'''
    # Calculate rolling statistic (median) without window shrinking
    df['STD-4-2_med'] = df['STD-4-2'].rolling(window=301, min_periods=1, center=True).median()
    
    # Calculate demedian. CH1_1_demed = CH_1 - CH_1_med
    df['STD-4-2_demed'] = df['STD-4-2'] - df['STD-4-2_med']

    '''PEAKS FINDING'''
     # Find peak indexes
    peaks_idx,_ = find_peaks(df['STD-4-2'],prominence=100)
    # Store peaks
    peaks = df.iloc[peaks_idx]
    # Reset rows index
    peaks.reset_index(drop=True, inplace=True)

    #If there is no peaks it goes back to the menu. For SSR files
    if peaks.empty:
        print('No peaks detected. Exiting to the menu...\n')
        plt.figure(figsize=(10, 6))
        plt.plot(df['DATETIME'],df['STD-4-2'],c='b')
        plt.title('STD-4-2 Data')
        plt.xticks(rotation=45)
        plt.show()
        return False

    '''PLOTTING'''

    plotResponse = input("Enter 'Y' if you want to plot the data: \n").lower()

    if plotResponse == 'y':
        print("Getting the plot... \n")

        plt.figure(figsize=(10, 6))
        plt.plot(df['DATETIME'],df['STD-4-2'],c='b')
        plt.plot(peaks['DATETIME'],peaks['STD-4-2'],'o',c='r')
        plt.title('IVS Plot: STD-4-2 Data')
        plt.xticks(rotation=45)
        plt.show()
    else:   print("Closing the program")

    # Printing peaks
    printOp1 = input("Enter 'Y' if you want to see the peaks of the signal: \n").lower()
    if printOp1 == "y":
        print(peaks[['X', 'Y','STD-4-2', 'STD-4-2_med', 'TIME']])
        print('\n')

     # Ask if the user wants to work on another file
    continue_choice = input("Would you like to process another sensor file or go to the menu? (Y/N): \n").lower()
    
    if continue_choice == 'y':
        return True
    else:
        print("Exiting to the menu...\n")
        return False

# Main loop for menu
def main_menu():
    while True:
        print("What type of file are you going to process?")
        print("1) IVS: Single EM61 sensor file (from 5 Coil System)")
        print("2) IVS: Regular EM61 file")
        print("3) Exit")
        menu_choice = input("Enter your option number or type 'Exit' to close the program:\n").lower()

        if menu_choice == '1':
            while True:
                if not EM61_5coil_ivs_file():
                    break
        elif menu_choice == '2':
            while True:
                if not EM61_ivs_file():
                    break
        elif menu_choice == '3' or menu_choice == 'exit':
            print('Closing the program...\n')
            break
        else:
            print("Invalid selection. Please try again.\n")

# Run the program
if __name__ == "__main__":
    main_menu()
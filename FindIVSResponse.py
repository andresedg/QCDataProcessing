import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

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


"""CLEANING AND FIXING FORMAT"""
# Checking if 'DATE' and 'TIME' columns exist to proceed
if 'DATE' in df.columns and 'TIME' in df.columns:
    df['DATE'] = df['DATE'] + ' ' + df['TIME']
    df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%y %H:%M:%S.%f')
else:
    print("Error: 'DATE' and/or 'TIME' columns not found.")
    
# Replacing empty spaces for NaN values
df = df.replace(r'^\s*$', np.nan, regex=True)

# Printing first lines of the data
printOp = input("Enter 'Y' if you want to see the header of the data: \n").lower()

if printOp == "y":
    print(df.head())
    print('\n')

# Find peak indexes
peaks_idx,_ = find_peaks(df['CH_1'],prominence=100)
# Store peaks
peaks = df.iloc[peaks_idx]
# Reset rows index
peaks.reset_index(drop=True, inplace=True)

printOp1 = input("Enter 'Y' if you want to see the peaks of the signal: \n").lower()
if printOp == "y":
    print(peaks.iloc[0])

"""PLOTTING"""

plotResponse = input("Enter 'Y' if you want to plot the data: \n").lower()

if plotResponse == 'y':
    print("Getting the plot... \n")

    plt.plot(df['DATE'],df['CH_1'],c='b')
    plt.plot(peaks['DATE'],peaks['CH_1'],'o',c='r')
    plt.title('IVS Plot')
    plt.show()
else:   print("Closing the program")
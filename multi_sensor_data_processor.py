import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import path_selector as ps # Function created in another py file (Not library)

def process_file():
    # Prompt the user to enter the file path    
    colnames = ['L1_coil_X', 'L1_coil_Y', 'L2_coil_X', 'L2_coil_Y', 'C_coil_X',
        'C_coil_Y', 'R1_coil_X', 'R1_coil_Y', 'R2_coil_X', 'R2_coil_Y',
        'QUAL_IND', 'DOP', 'HEIGHT', 'CH_1', 'CH_2', 'CH_3', 'CH_4',
        'EM61_CURRENT', 'EM61_VOLT', 'EM61_DELAY', 'CH_1.1', 'CH_2.1', 'CH_3.1',
        'CH_4.1', 'EM61_CURRENT.1', 'EM61_VOLT.1', 'EM61_DELAY.1', 'CH_1.2',    
        'CH_2.2', 'CH_3.2', 'CH_4.2', 'EM61_CURRENT.2', 'EM61_VOLT.2',
        'EM61_DELAY.2', 'CH_1.3', 'CH_2.3', 'CH_3.3', 'CH_4.3',
        'EM61_CURRENT.3', 'EM61_VOLT.3', 'EM61_DELAY.3', 'CH_1.4', 'CH_2.4',    
        'CH_3.4', 'CH_4.4', 'EM61_CURRENT.4', 'EM61_VOLT.4', 'EM61_DELAY.4',    
        'LINE', 'MARK', 'TIME', 'DATE']

    try:
        print('\nSelect file...')
        filepath = ps.select_file()
        # Attempt to read the file using Pandas
        df = pd.read_table(filepath, sep=r"\s+", skiprows=[0], names=colnames)
        dateOfData = df['DATE'].iloc[1]
        dateOfData = dateOfData.replace('/','')
        
        print(f"File loaded successfully!\n")

    except Exception as e:
        # If there is any error, print an error message
        print(f"Error: Unable to read the file or file not selected. {e}")
        return # If there is an error or the file selector is canceled close the program

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

    '''SPLIT DATA IN GROUPS'''
    # Identify each group and create sub dataframes
    group1 = df[['CH_1', 'CH_2', 'CH_3', 'CH_4',
                'EM61_CURRENT', 'EM61_VOLT', 'EM61_DELAY',
                'LINE', 'MARK', 'DATETIME']]

    group2 = df[['CH_1.1', 'CH_2.1', 'CH_3.1','CH_4.1',
                'EM61_CURRENT.1', 'EM61_VOLT.1','EM61_DELAY.1',
                'LINE', 'MARK', 'DATETIME']]

    group3 = df[['CH_1.2','CH_2.2', 'CH_3.2', 'CH_4.2', 
                'EM61_CURRENT.2', 'EM61_VOLT.2','EM61_DELAY.2',
                'LINE', 'MARK', 'DATETIME']]

    group4 = df[['CH_1.3', 'CH_2.3', 'CH_3.3', 'CH_4.3',
                'EM61_CURRENT.3', 'EM61_VOLT.3', 'EM61_DELAY.3',
                'LINE', 'MARK', 'DATETIME']]

    group5 = df[['CH_1.4', 'CH_2.4','CH_3.4', 'CH_4.4', 
                'EM61_CURRENT.4', 'EM61_VOLT.4', 'EM61_DELAY.4',
                'LINE', 'MARK', 'DATETIME']]

    # Remove NaN valuesin CH_1 column from each group.
    g1 = group1.dropna(subset=['CH_1'])
    g2 = group2.dropna(subset=['CH_1.1'])
    g3 = group3.dropna(subset=['CH_1.2'])
    g4 = group4.dropna(subset=['CH_1.3'])
    g5 = group5.dropna(subset=['CH_1.4'])

    # Renaming columns to ensure consistent naming for CH_1, CH_2, CH_3, CH_4
    g1 = g1.rename(columns={'CH_1': 'CH_1', 'CH_2': 'CH_2', 'CH_3': 'CH_3', 'CH_4': 'CH_4'})
    g2 = g2.rename(columns={'CH_1.1': 'CH_1', 'CH_2.1': 'CH_2', 'CH_3.1': 'CH_3', 'CH_4.1': 'CH_4'})
    g3 = g3.rename(columns={'CH_1.2': 'CH_1', 'CH_2.2': 'CH_2', 'CH_3.2': 'CH_3', 'CH_4.2': 'CH_4'})
    g4 = g4.rename(columns={'CH_1.3': 'CH_1', 'CH_2.3': 'CH_2', 'CH_3.3': 'CH_3', 'CH_4.3': 'CH_4'})
    g5 = g5.rename(columns={'CH_1.4': 'CH_1', 'CH_2.4': 'CH_2', 'CH_3.4': 'CH_3', 'CH_4.4': 'CH_4'})

    '''FINDING PEAK FOR EACH GROUP'''
    # Find peak indexes
    g1peaks_idx,_= find_peaks(g1['CH_1'].iloc[0:800],prominence=100)
    g2peaks_idx,_= find_peaks(g2['CH_1'].iloc[0:800],prominence=100)
    g3peaks_idx,_= find_peaks(g3['CH_1'].iloc[0:800],prominence=100)
    g4peaks_idx,_= find_peaks(g4['CH_1'].iloc[0:800],prominence=100)
    g5peaks_idx,_= find_peaks(g5['CH_1'].iloc[0:800],prominence=100)
    # Store peaks per group
    g1peaks = g1[['CH_1','DATETIME']].iloc[g1peaks_idx]
    g2peaks = g2[['CH_1','DATETIME']].iloc[g2peaks_idx]
    g3peaks = g3[['CH_1','DATETIME']].iloc[g3peaks_idx]
    g4peaks = g4[['CH_1','DATETIME']].iloc[g4peaks_idx]
    g5peaks = g5[['CH_1','DATETIME']].iloc[g5peaks_idx]

    '''DATAFRAME OF PEAKS'''
    # Adding the GROUPNUM column to each dataframe before concatenation
    g1peaks['GROUPNUM'] = 1
    g2peaks['GROUPNUM'] = 2
    g3peaks['GROUPNUM'] = 3
    g4peaks['GROUPNUM'] = 4
    g5peaks['GROUPNUM'] = 5

    peaks = pd.concat([g1peaks, g2peaks, g3peaks, g4peaks, g5peaks])
    # Reordering the columns, placing GROUPNUM first
    peaks = peaks[['GROUPNUM', 'CH_1', 'DATETIME']]

    # Sorting the dataframe by the DATE column first
    peaks = peaks.sort_values(by='DATETIME')

    # Defining the list of sensor names in the correct order
    sensor_names = ['L1', 'L2', 'C', 'R1', 'R2']

    # Assigning the sensor names based on the sorted order of the dates
    peaks['SENSOR'] = sensor_names

    # Reordering columns in this specific order
    peaks = peaks[['SENSOR', 'GROUPNUM', 'CH_1', 'DATETIME']]

    # Resetting the index again to keep it clean after sorting
    peaks.reset_index(drop=True, inplace=True)

    # Enter 'Y' to show the sensors corresponding to each group
    printOp1 = input("Enter 'Y' to show the sensors corresponding to each group: \n").lower()

    if printOp1 == "y":
        print(peaks)
        print('\n')

    '''PLOTTING'''
    plotResponse = input("Enter 'Y' if you want to plot the groups: \n")

    if plotResponse == 'Y' or plotResponse == 'y':  
        print("Getting the plot... \n")
        fig, (g1plot, g2plot,g3plot,g4plot,g5plot) = plt.subplots(5)
        fig.suptitle('5 Groups plot')
        # Group 1 subplot
        g1plot.plot(g1['DATETIME'].iloc[0:800].astype(str),g1['CH_1'].iloc[0:800].astype('Float64'))
        g1plot.plot(g1peaks['DATETIME'].astype(str),g1peaks['CH_1'].astype('Float64'),'o',c='r')
        g1plot.set_title("Group 1")
        g1plot.set_xticklabels([])
        # Group 2 subplot
        g2plot.plot(g2['DATETIME'].iloc[0:800].astype(str),g2['CH_1'].iloc[0:800].astype('Float64'),'tab:orange')
        g2plot.plot(g2peaks['DATETIME'].astype(str),g2peaks['CH_1'].astype('Float64'),'o',c='r')
        g2plot.set_title("Group 2")
        g2plot.set_xticklabels([])
        # Group 3 subplot
        g3plot.plot(g3['DATETIME'].iloc[0:800].astype(str),g3['CH_1'].iloc[0:800].astype('Float64'),'tab:green')
        g3plot.plot(g3peaks['DATETIME'].astype(str),g3peaks['CH_1'].astype('Float64'),'o',c='r')
        g3plot.set_title("Group 3")
        g3plot.set_xticklabels([])
        # Group 4 subplot
        g4plot.plot(g4['DATETIME'].iloc[0:800].astype(str),g4['CH_1'].iloc[0:800].astype('Float64'),'tab:red')
        g4plot.plot(g4peaks['DATETIME'].astype(str),g4peaks['CH_1'].astype('Float64'),'o',c='r')
        g4plot.set_title("Group 4")
        g4plot.set_xticklabels([])
        # Group 5 subplot
        g5plot.plot(g5['DATETIME'].iloc[0:800].astype(str),g5['CH_1'].iloc[0:800].astype('Float64'),'tab:purple')
        g5plot.plot(g5peaks['DATETIME'].astype(str),g5peaks['CH_1'].astype('Float64'),'o',c='r')
        g5plot.set_title("Group 5")
        g5plot.set_xticklabels([])
        fig.tight_layout()
        fig.set_figheight(6)
        fig.set_figwidth(10)
        plt.show(block = False)

    '''EXPORTING GROUP-SENSOR TABLE SORTED'''
    # Prompt to export group-sensor table
    exprotop = input("Enter 'Y' to export the group-sensor table: \n").lower()

    if exprotop == "y":
        try:
            print('Select folder...')
            filedirectory = ps.select_folder()

            # Check if the folder selection was successful
            if not filedirectory:
                print("Folder selection failed or was canceled.")
            else:
                inputfilename = input('Please enter the name of the file (Date included already): \n')
                sheet_name = input('Enter sheet name: \n')
                filename = f"{filedirectory}/{dateOfData}_{inputfilename}.xlsx"
                
                # Check if file exists
                if os.path.exists(filename):
                    with pd.ExcelWriter(filename, engine="openpyxl", mode="a") as writer:
                        # Name the sheet based on the sensor or some identifier
                        peaks.to_excel(writer, sheet_name=sheet_name, header=True, index=False)
                else:
                    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                        # Create a new file with the first sheet
                        peaks.to_excel(writer, sheet_name=sheet_name, header=True, index=False)

                print(f"Data exported successfully to {filename}\n")

        except Exception as e:
            print(f"Error while exporting: {e}")

    
    '''STORING SENSORS IN DATAFRAMES FOR EXPORTING'''
    # Create a dictionary of the group dataframes
    groups_dict = {1: g1, 2: g2, 3: g3, 4: g4, 5: g5}
    
    # Function to handle sensor merge with specific coil column names
    def merge_sensor(sensor_name, coil_x, coil_y, group_num):
        try:
            # Get the corresponding group dataframe from the dictionary
            group_merge = groups_dict[peaks['GROUPNUM'].iloc[group_num]]
            # Perform the merge with the specific coil columns for that sensor
            sensor_data = pd.merge(df[[coil_x, coil_y]], group_merge, left_index=True, right_index=True)
            sensor_data = pd.merge(sensor_data,df[['TIME','DATE']], left_index=True, right_index=True)
            sensor_data.reset_index(drop=True, inplace=True)
            return sensor_data
        except IndexError:
            print(f"Error: Group number {group_num + 1} is out of range.")
        except KeyError:
            print(f"Error: Group {group_num + 1} is not available in groups_dict.")

    # Function to plot sensor data
    def plot_sensor_data(sensor_data, sensor_name):
        try:
            plot_op = input("Do you want to plot the data? (Y/N): \n").lower()
            if plot_op == 'y':
                # Plotting the data for the selected sensor
                plt.figure(figsize=(10, 6))
                plt.plot(sensor_data['DATETIME'], sensor_data['CH_1'].astype('Float64'), color='blue')
                plt.title(f"Sensor {sensor_name}: CH_1 Data")
                plt.xlabel('Date')
                plt.ylabel('Amplitude')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
        except Exception as e:
            print(f"Error while plotting: {e}")

    # Function to export sensor data as a .xyz file
    def export_sensor_data(sensor_data, sensor_name):
        try:
            # Ask if the user wants to export the data
            export_op = input(f"Do you want to export the {sensor_name} data as a .xyz file? (Y/N): \n")
            if export_op.lower() == 'y':
                # Prepare the data for export (XYZ format with coil X and Y values)
                sensor_data_for_export = sensor_data
                # Ask the path and file name
                filedirectoyry = ps.select_folder()
                inputfilename = input('Please enter the name of the file (Date included already): ')
                filename = f"/{dateOfData}_{inputfilename}.xyz"
                # File exported with custom name: Path + Date + Name + .xyz
                sensor_data_for_export.to_csv(filedirectoyry + filename, sep=' ', index=False, header=True)
                print(f"Data exported successfully to {filename}\n")
            else:
                print(f"No data exported for sensor {sensor_name}.\n")
        except Exception as e:
            print(f"Error while exporting: {e}")

    while True:
        sensorSelec = input('What sensor do you want to work with? (L1, L2, C, R1, R2) or type "exit" to quit:\n')

        # Exit condition
        if sensorSelec.lower() == 'exit':
            print("Exiting to main menu...\n")
            break

        # Match case for different sensors, passing specific coil column names
        match sensorSelec.lower():
            case 'l1':
                sensor_data = merge_sensor('L1', 'L1_coil_X', 'L1_coil_Y', 0)    
                plot_sensor_data(sensor_data,'L1')
                export_sensor_data(sensor_data,'L1')
            case 'l2':
                sensor_data = merge_sensor('L2', 'L2_coil_X', 'L2_coil_Y', 1)
                plot_sensor_data(sensor_data,'L2')
                export_sensor_data(sensor_data,'L2')
            case 'c':
                sensor_data = merge_sensor('C', 'C_coil_X', 'C_coil_Y', 2)
                plot_sensor_data(sensor_data,'C')
                export_sensor_data(sensor_data,'C')
            case 'r1':
                sensor_data = merge_sensor('R1', 'R1_coil_X', 'R1_coil_Y', 3)
                plot_sensor_data(sensor_data,'R1')
                export_sensor_data(sensor_data,'R1')
            case 'r2':
                sensor_data = merge_sensor('R2', 'R2_coil_X', 'R2_coil_Y', 4)
                plot_sensor_data(sensor_data,'R2')
                export_sensor_data(sensor_data,'R2')
            case _:
                print("Invalid sensor selected. Please choose L1, L2, C, R1, or R2.")
    
    
    # Ask if the user wants to work on another file
    continue_choice = input("Would you like to process another file? (Y/N): \n").lower()
    
    if continue_choice == 'y':
        return True
    else:
        print("Exiting the program...\n")
        return False


# Main loop to handle multiple files
while True:
    if not process_file():
        break

# Sensor Data Analysis Tool

This Python script processes and analyzes sensor data by grouping it, finding peaks, and visualizing the data for further inspection. It supports multiple sensors and allows users to select and plot the data for specific sensors.

## Features

- Loads sensor data from a text file.
- Cleans and processes data, handling missing values.
- Groups data by different sensor groups.
- Identifies peaks in sensor readings.
- Plots sensor data and identified peaks.
- Allows exporting data for individual sensors.

## Prerequisites

Before running the script, ensure you have the following Python packages installed:

- `numpy`
- `pandas`
- `matplotlib`
- `scipy`

You can install them using pip:

```bash
pip install numpy pandas matplotlib scipy
```

## How to Use

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```

2. Navigate to the project folder:

   ```bash
   cd your-repo
   ```

3. Run the script:

   ```bash
   python main.py
   ```

4. When prompted, enter the path of the sensor data file. Ensure that the file follows the required format.

5. Optional user interactions:

   - To display the header of the data, type `Y` when prompted.
   - To plot the sensor data, type `Y` when prompted.
   - You can select which sensor data to analyze by choosing from: `L1`, `L2`, `C`, `R1`, or `R2`.

## Data Analysis

The script processes data from the following sensor groups:

- **L1**: Left sensor
- **L2**: Left sensor 2
- **C**: Center sensor
- **R1**: Right sensor 1
- **R2**: Right sensor 2

After loading and processing, the script detects peaks in the `CH_1` sensor reading for each group and displays the results in tabular and graphical formats.

## Plotting

When plotting is enabled, the script will generate a plot showing the sensor readings for the first 800 data points and mark the peaks.

## Example Data File

The file format should follow this column structure:

```
L1_coil_X, L1_coil_Y, L2_coil_X, L2_coil_Y, C_coil_X, C_coil_Y, ...
```

Ensure that the `DATE` and `TIME` columns exist and are in the format `MM/DD/YY HH:MM:SS.FFF`.

## License

## Pushing changes from local repository
Stage the changes:

```bash
git add .
```
```bash
git commit -m "Description of your changes"
```
```bash
git push origin main
```
After you push your changes, anyone who has access to the repository can run the following to get your updates:
```bash
git pull
```
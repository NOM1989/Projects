# Data Smoothing script for csv data (by Nicholas Michau, May 2024)
# Smooths out the data in a given column to be less 'jagged' by
# averaging out each value with a given number of its neighbors.

#####################################################
############### START OF CONFIGURATION ##############
#####################################################

# The file should be in the same folder as this script
FILENAME = "enter_file_name_here.csv"  # Must be a CSV file

# Which column of the csv holds the data you wish to smooth
# Eg. if your columns were: x,y,z,h to smooth the data in the z column you would enter 3 below:
SELECT_COLUMN = 3

# How much to smooth the data, larger numbers will have diminishing effects
# (How many neighboring values to consider when averaging)
# Recommended: 4
SMOOTHING_AMOUNT = 4

#####################################################
################ END OF CONFIGURATION ###############
#####################################################

import os
import csv


class Insight:
    """
    Calculate insights into the differences between the original and smoothed data.
    Helps visualise the effects of smoothing.
    """

    def __init__(self) -> None:
        self.ndigits = 6  # How many digits to round to when displaying
        self.min: float = float("inf")
        self.max: float = 0
        self.diffs: list = []

    def update(self, prev: float, curr: float):
        diff = abs(prev - curr)
        self.min = min(self.min, diff)
        self.max = max(self.max, diff)
        self.diffs.append(diff)

    def avg(self):
        return round(sum(self.diffs) / len(self.diffs), self.ndigits)

    def format(self):
        # Rounds the values to a sensible amount for displaying
        self.min = round(self.min, self.ndigits)
        self.max = round(self.max, self.ndigits)


# Get selected file paths
current_dir = os.path.dirname(__file__)
data_file_path = os.path.join(current_dir, FILENAME)
filename_no_ext, ext = os.path.splitext(data_file_path)
new_file_path = os.path.join(current_dir, f"{filename_no_ext}_smoothed{ext}")

# Selected column for smoothing
smooth_column_index = SELECT_COLUMN - 1

# How many adjacent values to include when calculating the local average
# Range will be (i-offset to i+offset)
offset = int(max(1, SMOOTHING_AMOUNT) / 2)

# Initialise insights
original_insights = Insight()
updated_insights = Insight()

previous_updated_row = None

print("Running Column Smoother - Ensure you have configured the options at the top of the script.")

if not os.path.exists(data_file_path):
    print(f"ERROR - File: {data_file_path} does not exist")
else:
    print(
        f"Current Settings: - Smoothing data in column=[{SELECT_COLUMN}] of file=[{data_file_path}] (Smoothing={SMOOTHING_AMOUNT})"
    )
    # Run through the data
    with open(data_file_path, "r", encoding="utf-8-sig", newline="") as original_file:
        with open(new_file_path, "w", encoding="utf-8-sig", newline="") as updated_file:
            reader = csv.reader(original_file)
            writer = csv.writer(updated_file)

            data = [tuple(map(float, row)) for row in list(reader)]

            print(
                f"\nCOLUMN CHECK:'{data[0][smooth_column_index]}' - Please ensure this is the first value in the column you wish to smooth. If not, adjust 'SELECTED_COLUMN' on line 15\n"
            )
            for i in range(len(data)):
                # grab data points around the current one
                local_data = [
                    row[smooth_column_index]
                    for row in data[max(0, i - offset) : min(len(data), i + 1 + offset)]
                ]
                # avg of those points
                local_mean = sum(local_data) / len(local_data)

                # Create the updated row and add it to a new file
                updated_row = list(data[i])
                updated_row[smooth_column_index] = local_mean
                # print(updated_row)

                # Calculate Insights
                if previous_updated_row:
                    original_insights.update(
                        data[i - 1][smooth_column_index], data[i][smooth_column_index]
                    )
                    updated_insights.update(
                        previous_updated_row[smooth_column_index],
                        updated_row[smooth_column_index],
                    )
                previous_updated_row = updated_row

                writer.writerow(updated_row)

    original_insights.format()
    updated_insights.format()
    print("Data insights for smoothed values:")
    print(
        f"> Origional Data:\n - Average difference: {original_insights.avg()}\n - Greatest difference: {original_insights.max}\n - Smallest difference: {original_insights.min}\n\t...between values\n"
    )
    print(
        f"> Smoothed Data:\n - Average difference: {updated_insights.avg()}\n - Greatest difference: {updated_insights.max}\n - Smallest difference: {updated_insights.min}\n\t...between values\n"
    )

    print(f"Generated new file with updated values at: {new_file_path}\nGood luck!")

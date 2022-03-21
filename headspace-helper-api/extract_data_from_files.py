from os import listdir
from pathlib import Path
from collections import OrderedDict
from . import root_dir


def find_solvent_data(i, j):
    """
    Extract the retention time, peak area, and peak height from the data files and return as either integer or
    float for every solvent in [solvents]. Only extract the data below the '[Peak Table (Ch1)]' line and stop
    extracting once a solvent has been found. If no solvent has been found return an empty tuple ("","","").
    """
    solvent_found = False
    peak_table_found = False

    with open(root_dir + "/Data/" + i) as data_file:

        lines = data_file.readlines()

        for line in lines:

            # Get data below [Peak Table (Ch1)] and ignore the rest:
            if "[Peak Table(Ch1)]" in line:
                peak_table_found = True

            if j in line and peak_table_found:
                rawdata = line.split()
                solvent_data = int(rawdata[4]), int(rawdata[5]), float(rawdata[1])
                solvent_found = True
                break

            if line == "\n" and peak_table_found:
                break

        return solvent_data if solvent_found else (0, 0, 0)


# Generate a list for every A, B, sample and CoA file:




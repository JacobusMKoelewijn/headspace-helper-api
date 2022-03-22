from . import root_dir
import glob


def find_solvent_data(solvent_name, file_type):
    """
    Extract the retention time, peak area, and peak height from the data files and return as either integer or
    float for every solvent in [solvents]. Only extract the data below the '[Peak Table (Ch1)]' line and stop
    extracting once a solvent has been found. If no solvent has been found return an empty tuple ("","","").
    """

    solvent_found = False
    peak_table_found = False

    for name in glob.glob(root_dir + "/input_data/" + f"{file_type}*.txt"):

        with open(name) as data_file:

            lines = data_file.readlines()

            for line in lines:

                # Get data below [Peak Table (Ch1)] and ignore the rest:
                if "[Peak Table(Ch1)]" in line:
                    peak_table_found = True

                if solvent_name in line and peak_table_found:
                    rawdata = line.split()
                    solvent_data = int(rawdata[4]), int(rawdata[5]), float(rawdata[1])
                    solvent_found = True
                    break

                if line == "\n" and peak_table_found:
                    break

            return solvent_data if solvent_found else (0, 0, 0)


class Solvent:
    def __init__(self, solvent_coa_data):
        self.name = solvent_coa_data[0]
        self.manufacturer = solvent_coa_data[1]
        self.catalog_number = solvent_coa_data[2]
        self.lot_number = solvent_coa_data[3]
        self.expiration_date = solvent_coa_data[4][:3] + " " + solvent_coa_data[4][3:]
        self.purity = float(solvent_coa_data[5][:-5])

        # print(self.name, self.manufacturer, self.catalog_number, self.lot_number, self.expiration_date, self.purity)

        self.a1 = find_solvent_data(self.name, "A1")
        self.a2 = find_solvent_data(self.name, "A2")
        self.a3 = find_solvent_data(self.name, "A3")
        self.a4 = find_solvent_data(self.name, "A4")
        self.a5 = find_solvent_data(self.name, "A5")
        self.a6 = find_solvent_data(self.name, "A6")
        self.a7 = find_solvent_data(self.name, "A7")
        self.a8 = find_solvent_data(self.name, "A8")
        self.a9 = find_solvent_data(self.name, "A9")
        self.a10 = find_solvent_data(self.name, "A10")
        self.a11 = find_solvent_data(self.name, "A11")
        self.a12 = find_solvent_data(self.name, "A12")
        self.b3_1 = find_solvent_data(self.name, "B3.1")
        self.b3_2 = find_solvent_data(self.name, "B3.2")
        self.b3_3 = find_solvent_data(self.name, "B3.3")
        self.b3_4 = find_solvent_data(self.name, "B3.4")
        self.b3_5 = find_solvent_data(self.name, "B3.5")
        self.b3_6 = find_solvent_data(self.name, "B3.6")
        self.b3_7 = find_solvent_data(self.name, "B3.7")
        self.b3_8 = find_solvent_data(self.name, "B3.8")


class Sample:
    def __init__(self, sample_data):
        self.name = sample_data
        print(self.name)

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

            return solvent_data if solvent_found else None


class Sample:
    """
    Class to set sample attributes used in Solvent class.
    """
    samples = []

    def __init__(self, sample_code):
        self.sample_code = sample_code
        self.sample_tag_1 = None
        self.sample_tag_2 = None
        self.sample_tag_3 = None
        self.sample_tag_S_A4 = None
        self.sample_tag_S_A5 = None
        self.sample_tag_S_A6 = None

class Solvent:
    """
    Class to store retention time, peak area, and peak height as solvent attributes.
    """
    solvents = []

    def __init__(self, solvent_coa_data):

        # Set attributes for solvent CoA data:
        self.name = solvent_coa_data[0]
        self.manufacturer = solvent_coa_data[1]
        self.catalog_number = solvent_coa_data[2]
        self.lot_number = solvent_coa_data[3]
        self.expiration_date = solvent_coa_data[4][:3] + " " + solvent_coa_data[4][3:]
        self.purity = float(solvent_coa_data[5][:-5])

        # Set attributes for A1-A12 data:
        for i in range(13):
            setattr(self, "a" + f"{i}", find_solvent_data(self.name, "A" + f"{i}"))

        # Set attributes for B3.1-B3.8 data:
        for i in range(9):
            setattr(self, "b3_" + f"{i}", find_solvent_data(self.name, "B3." + f"{i}"))

        # Set attributes for every sample tag data:
        for i in Sample.samples:
            i.sample_tag_1 = find_solvent_data(self.name, f"{i.sample_code}-1")
            i.sample_tag_2 = find_solvent_data(self.name, f"{i.sample_code}-2")
            i.sample_tag_3 = find_solvent_data(self.name, f"{i.sample_code}-3")
            i.sample_tag_S_A4 = find_solvent_data(self.name, f"{i.sample_code}-S-A4")
            i.sample_tag_S_A5 = find_solvent_data(self.name, f"{i.sample_code}-S-A5")
            i.sample_tag_S_A6 = find_solvent_data(self.name, f"{i.sample_code}-S-A6")

        # self.print_data()

    def print_data(self):
        print("Solvent objects")
        print(Solvent.solvents)
        print("Sample objects")
        print(Sample.samples)
        print("### CoA Data ###")
        print(self.name, self.manufacturer, self.catalog_number, self.lot_number, self.expiration_date, self.purity)
        print("### A-file Data ###")
        print(self.a1, self.a2, self.a3, self.a4, self.a5, self.a6,
              self.a7, self.a8, self.a9, self.a10, self.a11, self.a12)
        print("### B-file Data ###")
        print(self.b3_1, self.b3_2, self.b3_3, self.b3_4, self.b3_5, self.b3_6, self.b3_7, self.b3_8)
        print("### sample tag Data ###")
        for i in Sample.samples:
            print(i.sample_code)
            print(i.sample_tag_1)
            print(i.sample_tag_2)
            print(i.sample_tag_3)
            print(i.sample_tag_S_A4)
            print(i.sample_tag_S_A5)
            print(i.sample_tag_S_A6)
        print("###################################")
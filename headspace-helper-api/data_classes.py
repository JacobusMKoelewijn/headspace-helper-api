import re
# https://stackoverflow.com/questions/12008991/create-instance-of-class-in-another-class-with-generic-example
# https://livebook.manning.com/book/the-quick-python-book-second-edition/chapter-20/56
class FileTypes(): #FileType class
    
    _regex_a_file = "(^A[1-8]_)"
    _regex_b_file = "(^B3.[1-8]_)"
    _regex_sample_file = "(^[A-Z]{3}([0-9]{5}|[0-9]{8})-[0-9]{1,3}-([A-Z]|[0-9]{1,3})-([1-3]|S-A[4-6]))"

    
    def __init__(self, txt_files, temp_dir):

        self.temp_dir = temp_dir
        
        for file in txt_files:
            correct_a_format = re.search(FileTypes._regex_a_file, file)
            if correct_a_format:
                setattr(FileTypes, correct_a_format.group(), file)
    
        print(FileTypes.__dict__)


    # __setitem make use of.
    # def __check(self, element):



        # pattern = re.compile(Files._regex_a_file)
        # self.a_files = []

        # print(uploaded_files)

        # for file in uploaded_files:
            # self.a1_file = re.match("A1_", file)
        
        # for file
        # Use raise Error
        # print(self.a1_file)

        # https://stackoverflow.com/questions/37974047/if-any-strings-in-a-list-match-regex

        # for file in file_names:

            # a_file_format = re.findall(Files._regex_a_file, file)
        # if a_file_format:
            # self.a_files = AFile(file_name)
        
        # print(a_file_format)
        # self.a1_file = re.search("(^A1_)", file_name)

        # print(self.a1_file)
    
    def find_data(self, solvent, file_name):

        with open(self.temp_dir + "/" + file_name) as data_file:
            print("hallo")
            
            solvent_found = False
            peak_table_found = False

            lines = data_file.readlines()

            for line in lines:

                # Get data below [Peak Table (Ch1)] and ignore the rest:
                if "[Peak Table(Ch1)]" in line:
                    peak_table_found = True

                if solvent in line and peak_table_found:
                    rawdata = line.split()
                    # Change rawdate in keywords
                    solvent_data = int(rawdata[4]), int(rawdata[5]), float(rawdata[1])
                    solvent_found = True
                    break

                if line == "\n" and peak_table_found:
                    break

            return solvent_data if solvent_found else (0, 0, 0)


        # b_file_format = re.search(Files._regex_b_file, file_name)
        # if b_file_format:
        #     BFile(file_name)
            

class Sample:
    """
    Class to store tag attributes for every unique sample and every solvent.
    """

    def __init__(self, sample_code, sample_data):
        self.sample_code = sample_code

        for key, val in sample_data.items():
            self.__dict__[key] = val


class Diluent:
    """
    Class to store information found in CoA data for Diluent.
    """

    def __init__(self, solvent_coa_data):
        self.name = solvent_coa_data[0]
        self.manufacturer = solvent_coa_data[1]
        self.catalog_number = solvent_coa_data[2]
        self.lot_number = solvent_coa_data[3]
        self.expiration_date = solvent_coa_data[4][:3] + " " + solvent_coa_data[4][3:]
        self.purity = float(solvent_coa_data[5][:-5])


class Solvent(Diluent):
    """
    Class to store information found in CoA data for solvent and in addition the retention time, peak area, and peak
    height as solvent attributes.
    """

    # def __init__(self, solvent_coa_data, a_file_data, b_file_data):
    def __init__(self, file_types):
        # super().__init__(solvent_coa_data)

        self.a1 = FileTypes.find_data(file_types, "Ethanol", file_types.A1_)
        self.a2 = None
        self.a3 = None
        self.a4 = None
        self.a5 = None
        self.a6 = None
        self.a7 = None
        self.a8 = None

        print(self.a1)

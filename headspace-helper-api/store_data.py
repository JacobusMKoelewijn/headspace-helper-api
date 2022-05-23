import re


class Files:
    _regex_a_file = "(^A[1-8]_)"
    _regex_b_file = "(^B3.[1-8]_)"
    _regex_sample_file = "(^[A-Z]{3}([0-9]{5}|[0-9]{8})-[0-9]{1,3}-([A-Z]|[0-9]{1,3})-([1-3]|S-A[4-6]))"
    incorrect_files = []
    unique_sample_codes = set()

    def __init__(self, txt_files, coa_files, temp_dir):

        self.temp_dir = temp_dir
        self.txt_files = txt_files
        self.coa_files = coa_files

    def __getattr__(self, name):
        try:
            return self.__getattr__.name
        except AttributeError:
            return ""

    def check_file_requirements(self):
        """
        Check if uploaded files specify the requirements to create a headspace Excel workbook.
        If not, return an instance of the Feedback class with the specified problem, solution and additional information.
        """

        feedback = Feedback()

        if not self.coa_files:
            feedback.problem = "No CoA files provided."
            feedback.solution = "Please upload a CoA .pdf file for each solvent."

        elif len(self.coa_files) > 12:
            feedback.problem = "More then 12 CoA files detected!"
            feedback.solution = "Please upload no more then 12 solvent CoA .pdf files."

        elif len(self.get_unique_sample_code()) > 5:
            feedback.problem = "More then 5 samples provided!"
            feedback.solution = "Please upload no more then 5 sample measurements."

        else:
            for file in self.txt_files:
                correct_format = re.search(Files._regex_sample_file + "|" +
                                           Files._regex_a_file + "|" +
                                           Files._regex_b_file, file)
                if not correct_format:
                    Files.incorrect_files.append(file)

            for file in self.coa_files:
                if not len(file.split()) == 6:
                    Files.incorrect_files.append(file)

            if Files.incorrect_files:
                feedback.problem = "Incorrect file format!"
                feedback.solution = "Please correct the following file names:."
                feedback.information = Files.incorrect_files
            else:
                feedback.all_files_correct = True

        return feedback

    def get_unique_sample_code(self):
        """
        Return a set with unique sample codes extracted from all .txt files.
        """

        for file in self.txt_files:
            unique_sample_code = re.search(Files._regex_sample_file[1:59], file)

            if unique_sample_code:
                Files.unique_sample_codes.add(unique_sample_code.group())

        return Files.unique_sample_codes

    def set_filenames_as_attributes(self):
        for file in self.txt_files:

            a_file = re.search(Files._regex_a_file, file)
            if a_file:
                setattr(Files, a_file.group()[:-1], file)

            b_file = re.search(Files._regex_b_file, file)
            if b_file:
                setattr(Files, b_file.group()[:-1].replace(".", "_"), file)

            sample_file = re.search(Files._regex_sample_file, file)
            if sample_file:
                setattr(Files, sample_file.group(), file)

    def extract_data(self, solvent, filename):
        """
        Extract the peak retention time, area, and height from uploaded .txt files and return as a dictionary
        for every solvent object. Only extract the data below the '[Peak Table (Ch1)]' line and stop
        extracting once a solvent has been found.
        """

        peak_data = {"retention time": None, "area": None, "height": None}

        try:
            with open(self.temp_dir + "/" + filename) as file:

                peak_table_found = False

                lines = file.readlines()

                for line in lines:

                    # Get data below line containing "[Peak Table (Ch1)]" in file and ignore the rest:
                    if "[Peak Table(Ch1)]" in line:
                        peak_table_found = True

                    if solvent in line and peak_table_found:
                        raw_data = line.split()
                        peak_data["retention time"] = float(raw_data[1])
                        peak_data["area"] = int(raw_data[4])
                        peak_data["height"] = int(raw_data[5])
                        break

                    if line == "\n" and peak_table_found:
                        break

                return peak_data

        except PermissionError:
            return peak_data


class Sample:
    """
    Store tag attributes for every unique sample and every solvent.
    """

    def __init__(self, solvent_objects, sample_code, files):
        self.sample_code = sample_code

        for solvent in solvent_objects:
            setattr(self, solvent.solvent_name + "_tag_1",
                    files.extract_data(solvent.solvent_name, Files.__dict__[sample_code + "-1"]))
            setattr(self, solvent.solvent_name + "_tag_2",
                    files.extract_data(solvent.solvent_name, Files.__dict__[sample_code + "-2"]))
            setattr(self, solvent.solvent_name + "_tag_3",
                    files.extract_data(solvent.solvent_name, Files.__dict__[sample_code + "-3"]))
            setattr(self, solvent.solvent_name + "_tag_S_A4",
                    files.extract_data(solvent.solvent_name, Files.__dict__[sample_code + "-S-A4"]))
            setattr(self, solvent.solvent_name + "_tag_S_A5",
                    files.extract_data(solvent.solvent_name, Files.__dict__[sample_code + "-S-A5"]))
            setattr(self, solvent.solvent_name + "_tag_S_A6",
                    files.extract_data(solvent.solvent_name, Files.__dict__[sample_code + "-S-A6"]))


class Diluent:
    """
    Store information found in CoA data for diluent.
    """

    def __init__(self, solvent_coa_data):
        self.solvent_name = solvent_coa_data[0]
        self.manufacturer = solvent_coa_data[1]
        self.catalog_number = solvent_coa_data[2]
        self.lot_number = solvent_coa_data[3]
        self.expiration_date = solvent_coa_data[4][:3] + " " + solvent_coa_data[4][3:]
        self.purity = float(solvent_coa_data[5][:-5])


class Solvent(Diluent):
    """
    Store information found in CoA data for solvent.
    Set attributes with peak_data dictionary by calling the extract_data method.
    """

    def __init__(self, solvent_coa_data, files):
        super().__init__(solvent_coa_data)

        self.a1 = files.extract_data(self.solvent_name, files.A1)
        self.a2 = files.extract_data(self.solvent_name, files.A2)
        self.a3 = files.extract_data(self.solvent_name, files.A3)
        self.a4 = files.extract_data(self.solvent_name, files.A4)
        self.a5 = files.extract_data(self.solvent_name, files.A5)
        self.a6 = files.extract_data(self.solvent_name, files.A6)
        self.a7 = files.extract_data(self.solvent_name, files.A7)
        self.a8 = files.extract_data(self.solvent_name, files.A8)

        self.b3_1 = files.extract_data(self.solvent_name, files.B3_1)
        self.b3_2 = files.extract_data(self.solvent_name, files.B3_2)
        self.b3_3 = files.extract_data(self.solvent_name, files.B3_3)
        self.b3_4 = files.extract_data(self.solvent_name, files.B3_4)
        self.b3_5 = files.extract_data(self.solvent_name, files.B3_5)
        self.b3_6 = files.extract_data(self.solvent_name, files.B3_6)
        self.b3_7 = files.extract_data(self.solvent_name, files.B3_7)
        self.b3_8 = files.extract_data(self.solvent_name, files.B3_8)


class Feedback:
    def __init__(self):
        self.all_files_correct = False
        self.problem = None
        self.solution = None
        self.information = None

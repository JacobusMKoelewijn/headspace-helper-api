class Files:
    """

    """
    pass


class AFile:
    _regex_a_file = "(^A[1-8]_)"

    def __init__(self, file_name):
        self.file_name = file_name

        print(self.file_name)


class BFile:
    pass


class SampleFile:
    pass


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

    def __init__(self, solvent_coa_data, a_file_data, b_file_data):
        super().__init__(solvent_coa_data)

        for key, val in a_file_data.items():
            self.__dict__[key] = val

        for key, val in b_file_data.items():
            self.__dict__[key] = val

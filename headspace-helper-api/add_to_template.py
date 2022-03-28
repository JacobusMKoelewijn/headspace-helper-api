# To suppress a warning by openpyxl.
import warnings

warnings.simplefilter("ignore")

import sys, os
import openpyxl
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.trendline import Trendline, TrendlineLabel
from openpyxl.chart.data_source import NumFmt
from openpyxl.chart.text import RichText
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, Font
from . import root_dir
from .solvent_data import Solvent


# def resource_path(relative_path):
#     """ Get absolute path to Excel template file. """
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)


class Template:
    def __init__(self):
        self.collected_messages = "test"
        # self.solvents = ""
        self.wb = openpyxl.load_workbook(root_dir + "/output_data/HS_Quantification Template (HH v 1.3).xlsx")

    def create_solvent_sheets(self):
        """ Create a sheet for every solvent in [solvents] """
        # from .extract_data_from_files import solvents

        if Solvent.solvents:
            self.collected_messages = "Solvents found"
        else:
            self.collected_messages = "No solvents found"
            # self.collected_messages = "No CoA of any solvent has been provided!\nExtraction procedure can't continue."
            # return (self.collected_messages)

        # if len(self.solvents) <= 12:
        #     pass
        # else:
        #     self.collected_messages = "More then 12 solvent CoAs have been provided!\nExtraction procedure can't continue."
        #     return (self.collected_messages)

        # Add a reference to each cell that needs a reference:
        # for j, i in enumerate(self.solvents):
        #     for z in cells_with_reference[9:]:
        #         self.wb[f"solvent {j + 2}"][z] = f"='{self.solvents[0]}'!{z}"
        #     self.wb[f"solvent {j + 1}"].title = i
        #
        # for z in cells_with_reference[:9]:
        #     self.wb["Analytical Report"][z] = f"='{self.solvents[0]}'!{z}"

        # Remove unused sheets (based on 12 + 1 solvent sheets):
        # remaining_sheets = 13 - len(self.solvents)
        # for i in range(remaining_sheets):
        #     self.wb.remove(self.wb[f"solvent {i + len(self.solvents) + 1}"])
        #
        # self.solvent_sheets = {i: self.wb[i] for i in self.solvents}

        # self.plot_chart()

    # def plot_chart(self):
    #     """ Generate a chart and specify the layout for all solvent sheets """
    #
    #     for i in self.solvents:
    #         # Find x and y-values:
    #         xvalues = Reference(self.wb[i], min_col=5, min_row=62, max_row=69)
    #         yvalues = Reference(self.wb[i], min_col=7, min_row=62, max_row=69)
    #
    #         # Instantiate chart object and set properties:
    #         chart = ScatterChart()
    #         chart.x_axis.title = "Concentration (µg/mL)"
    #         chart.x_axis.majorGridlines = None
    #         chart.x_axis.numFmt = '0'
    #         chart.y_axis.title = "Peak area (a.u.*s)"
    #         chart.y_axis.majorGridlines.spPr = GraphicalProperties(noFill='True')
    #         chart.y_axis.majorGridlines.spPr.ln = LineProperties(solidFill='C5E3F5')
    #         chart.legend = None
    #
    #         # Instantiate series object and set properties:
    #         series = Series(yvalues, xvalues)
    #         series.marker = openpyxl.chart.marker.Marker('circle')
    #         series.graphicalProperties.line.noFill = True
    #         line_property = LineProperties(solidFill='A02D96')
    #         graphical_property = GraphicalProperties(ln=line_property)
    #         font_property = Font(typeface='Calibri Light')
    #         character_property = CharacterProperties(latin=font_property, sz=900, solidFill='FF0000')
    #         paragraph_property = ParagraphProperties(defRPr=character_property)
    #         richtext_property = RichText(p=[Paragraph(pPr=paragraph_property, endParaRPr=character_property)])
    #         number_format_property = NumFmt(formatCode='0.0000E+00')
    #         trendline_label = TrendlineLabel(txPr=richtext_property, numFmt=number_format_property)
    #         series.trendline = Trendline(dispRSqr=True, dispEq=True, spPr=graphical_property,
    #                                      trendlineLbl=trendline_label)
    #         chart.series.append(series)
    #
    #         # Add chart to sheet.
    #         self.wb[i].add_chart(chart, "N61")
    #
    #     self.add_coa_data()
    #
    # def add_coa_data(self):
    #     from .extract_data_from_files import solvents_CoA_data
    #
    #     if "NMP" in solvents_CoA_data.keys():
    #         self.diluent = "NMP"
    #     elif "DMAC" in solvents_CoA_data.keys():
    #         self.diluent = "DMAC"
    #     elif "DMI" in solvents_CoA_data.keys():
    #         self.diluent = "DMI"
    #     else:
    #         self.diluent = "diluent"
    #
    #     # Add CoA data for 1. Diluent:
    #     try:
    #         self.solvent_sheets[self.solvents[0]]["A22"] = self.diluent
    #         self.solvent_sheets[self.solvents[0]]["B22"] = solvents_CoA_data[self.diluent][0]
    #         self.solvent_sheets[self.solvents[0]]["C22"] = solvents_CoA_data[self.diluent][1]
    #         self.solvent_sheets[self.solvents[0]]["D22"] = solvents_CoA_data[self.diluent][2]
    #         self.collected_messages += f"The diluent is {self.diluent}!\n\n"
    #     except:
    #         self.collected_messages += f"CoA of {self.diluent} not provided or incorect format is used.\n"
    #
    #     # Add CoA for 2. Reference standards:
    #     for i in self.solvents:
    #
    #         try:
    #             self.solvent_sheets[i]["A27"] = i
    #             self.solvent_sheets[i]["B27"] = solvents_CoA_data[i][0]
    #             self.solvent_sheets[i]["C27"] = solvents_CoA_data[i][1]
    #             self.solvent_sheets[i]["D27"] = solvents_CoA_data[i][2]
    #             self.solvent_sheets[i]["F27"] = solvents_CoA_data[i][3][:3] + " " + solvents_CoA_data[i][3][3:]
    #             self.solvent_sheets[i]["E27"] = float(solvents_CoA_data[i][4][:-5])
    #         except:
    #             self.collected_messages += f"Something went wrong for {i}.\nIs the correct format used for the CoA file?"
    #             return (self.collected_messages)
    #
    #     self.collected_messages += f"A total of {len(self.solvents)} {'solvents CoAs' if len(self.solvents) > 1 else 'solvent CoA'} has been found.\n"
    #
    #     self.add_area_height_data_A()
    #
    # def add_area_height_data_A(self):
    #
    #     from .extract_data_from_files import collected_A_files, solvents_area_height_A
    #     number_of_A_files = len(collected_A_files)
    #
    #     # 6. Add peak area and peak height data for 6. Calibration curve:
    #     for i in self.solvents:
    #
    #         if ((number_of_A_files) < 8) or (number_of_A_files > 12):
    #             self.collected_messages += "Between 8 or 12 A-files have to be supplied.\nExtraction procedure can't continue."
    #             return self.collected_messages
    #
    #         for j in range(number_of_A_files - 4):
    #             self.solvent_sheets[self.solvents[0]][f"A{73 - j - (12 - number_of_A_files)}"] = f"A{j + 1}"
    #             self.solvent_sheets[i][f"F{73 - j - (12 - number_of_A_files)}"] = solvents_area_height_A[i][j][0]
    #
    #         for j in range(4):
    #             self.solvent_sheets[self.solvents[0]][f"A{65 - j}"] = f"A{j + number_of_A_files - 3}"
    #             self.solvent_sheets[i][f"F{65 - j}"] = solvents_area_height_A[i][j - 4][0]
    #             self.solvent_sheets[i][f"I{65 - j}"] = solvents_area_height_A[i][j - 4][1]
    #
    #     self.collected_messages += f"Data of files A1 to A{number_of_A_files} have been transferred succesfully!\n"
    #
    #     self.add_area_height_data_B()
    #
    # def add_area_height_data_B(self):
    #
    #     from .extract_data_from_files import collected_B_files, solvents_area_height_B
    #     number_of_B_files = len(collected_B_files)
    #
    #     if not number_of_B_files > 0:
    #         self.collected_messages += "No B-Files have been supplied!\n"
    #         self.add_sample_data()
    #         return (self.collected_messages)
    #
    #     for i in self.solvents:
    #
    #         # Add peak area and retention time data for 7. Repeatability and control:
    #         for j in range(3):
    #             self.solvent_sheets[i][f"G{84 + j}"] = solvents_area_height_B[i][j][2]
    #             self.solvent_sheets[i][f"H{84 + j}"] = solvents_area_height_B[i][j][0]
    #
    #         # Add peak area for 8. Data for bracketing control:
    #         for j in range(number_of_B_files - 3):
    #             self.solvent_sheets[i][f"G{95 + j}"] = solvents_area_height_B[i][3 + j][0]
    #
    #     self.collected_messages += f"Data of files B3.1 to B3.{number_of_B_files} have been transferred succesfully!\n"
    #
    #     self.add_sample_data()
    #
    # def add_sample_data(self):
    #
    #     from .extract_data_from_files import unique_samples, solvents_area_height_samples
    #     number_of_unique_samples = len(unique_samples)
    #
    #     if not number_of_unique_samples > 0:
    #         self.collected_messages += "No sample data has been supplied.\n"
    #         self.save_template()
    #         return (self.collected_messages)
    #
    #     if number_of_unique_samples > 5:
    #         self.collected_messages += "Between 0 or 5 sample files have to be supplied.\nExtraction procedure can't continue."
    #         return (self.collected_messages)
    #
    #     for j in range(len(unique_samples)):
    #         self.solvent_sheets[self.solvents[0]][f"A{105 + (j * 6)}"] = unique_samples[j]
    #
    #     for i in self.solvents:
    #         for j in range(len(unique_samples)):
    #
    #             for z in range(len(solvents_area_height_samples[unique_samples[j]][i])):
    #                 self.solvent_sheets[i][f"I{105 + z + (j * 6)}"] = \
    #                 solvents_area_height_samples[unique_samples[j]][i][z][0]
    #
    #             # The values for S-A6 and S-A4 have to be manually switched if samples exist with S-files:
    #             if len(solvents_area_height_samples[unique_samples[j]][i]) == 6:
    #                 self.solvent_sheets[i][f"I{108 + (j * 6)}"] = solvents_area_height_samples[unique_samples[j]][i][5][
    #                     0]
    #                 self.solvent_sheets[i][f"I{110 + (j * 6)}"] = solvents_area_height_samples[unique_samples[j]][i][3][
    #                     0]
    #
    #     self.collected_messages += f"Data of {number_of_unique_samples} sample{'s have' if number_of_unique_samples > 1 else ' has'} been transferred succesfully!\n"
    #
    #     self.save_template()
    #
    # def save_template(self):
    #     self.wb.save("HS_Quantification Template (HH v 1.3) (processed).xlsx")
    #     self.collected_messages += "\nA processed Template file has been created!\n"
    #
    def return_collected_messages(self):
        return self.collected_messages

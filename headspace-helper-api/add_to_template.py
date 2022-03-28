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
from . import cells_with_reference
from .solvent_data import Solvent, Diluent, Sample


class Template:
    template_constructed = False

    def __init__(self):
        self.collected_messages = ""
        self.wb = openpyxl.load_workbook(root_dir + "/template_file/HS_Quantification Template (HH v 2.0).xlsx")

    def create_solvent_sheets(self):
        """ Create a sheet for every solvent in Solvent.solvents """

        if Solvent.solvents:
            self.collected_messages = f"<li><span style='color: #48dbfb;'>{len(Solvent.solvents)}</span> solvents found.</li>"
        else:
            self.collected_messages = "<li>No CoAs have been provided.</li>"
            return

        if len(Solvent.solvents) <= 12:
            pass
        else:
            self.collected_messages = "More then 12 CoAs were provided!"
            return

        # Add a reference to each cell that needs a reference:
        for j, i in enumerate(Solvent.solvents):
            for z in cells_with_reference[9:]:
                self.wb[f"solvent {j + 2}"][z] = f"='{Solvent.solvents[0].name}'!{z}"
            self.wb[f"solvent {j + 1}"].title = i.name

        for z in cells_with_reference[:9]:
            self.wb["Analytical Report"][z] = f"='{Solvent.solvents[0].name}'!{z}"

        # Remove unused sheets (based on 12 + 1 solvent sheets):
        remaining_sheets = 13 - len(Solvent.solvents)
        for i in range(remaining_sheets):
            self.wb.remove(self.wb[f"solvent {i + len(Solvent.solvents) + 1}"])

        self.solvent_sheets = {i.name: self.wb[i.name] for i in Solvent.solvents}

        self.plot_chart()

    def plot_chart(self):
        """ Generate a chart and specify the layout for all solvent sheets """

        for i in Solvent.solvents:
            # Find x and y-values:
            xvalues = Reference(self.wb[i.name], min_col=5, min_row=62, max_row=69)
            yvalues = Reference(self.wb[i.name], min_col=7, min_row=62, max_row=69)

            # Instantiate chart object and set properties:
            chart = ScatterChart()
            chart.x_axis.title = "Concentration (µg/mL)"
            chart.x_axis.majorGridlines = None
            chart.x_axis.numFmt = '0'
            chart.y_axis.title = "Peak area (a.u.*s)"
            chart.y_axis.majorGridlines.spPr = GraphicalProperties(noFill='True')
            chart.y_axis.majorGridlines.spPr.ln = LineProperties(solidFill='C5E3F5')
            chart.legend = None

            # Instantiate series object and set properties:
            series = Series(yvalues, xvalues)
            series.marker = openpyxl.chart.marker.Marker('circle')
            series.graphicalProperties.line.noFill = True
            line_property = LineProperties(solidFill='A02D96')
            graphical_property = GraphicalProperties(ln=line_property)
            font_property = Font(typeface='Calibri Light')
            character_property = CharacterProperties(latin=font_property, sz=900, solidFill='FF0000')
            paragraph_property = ParagraphProperties(defRPr=character_property)
            richtext_property = RichText(p=[Paragraph(pPr=paragraph_property, endParaRPr=character_property)])
            number_format_property = NumFmt(formatCode='0.0000E+00')
            trendline_label = TrendlineLabel(txPr=richtext_property, numFmt=number_format_property)
            series.trendline = Trendline(dispRSqr=True, dispEq=True, spPr=graphical_property,
                                         trendlineLbl=trendline_label)
            chart.series.append(series)

            # Add chart to sheet.
            self.wb[i.name].add_chart(chart, "N61")

        self.add_coa_data()

    def add_coa_data(self):

        # Add CoA data for 1. Diluent:
        try:
            self.solvent_sheets[Solvent.solvents[0].name]["A22"] = Diluent.diluent.diluent_name
            self.solvent_sheets[Solvent.solvents[0].name]["B22"] = Diluent.diluent.diluent_manufacturer
            self.solvent_sheets[Solvent.solvents[0].name]["C22"] = Diluent.diluent.diluent_catalog_number
            self.solvent_sheets[Solvent.solvents[0].name]["D22"] = Diluent.diluent.diluent_lot_number
            self.collected_messages += f"<li>The diluent is <span style='color: #48dbfb;'>{Diluent.diluent.diluent_name}</span>!</li>"
        except:
            self.collected_messages += f"<li>CoA of diluent not provided or incorrect format is used.</li>"

        # Add CoA for 2. Reference standards:
        for i in Solvent.solvents:

            try:
                self.solvent_sheets[i.name]["A27"] = i.name
                self.solvent_sheets[i.name]["B27"] = i.manufacturer
                self.solvent_sheets[i.name]["C27"] = i.catalog_number
                self.solvent_sheets[i.name]["D27"] = i.lot_number
                self.solvent_sheets[i.name]["F27"] = i.expiration_date
                self.solvent_sheets[i.name]["E27"] = i.purity
            except:
                self.collected_messages += f"Something went wrong for <span style='color: #48dbfb;'>{i.name}</span>."

        self.add_area_height_data_a()

    def add_area_height_data_a(self):

        # 6. Add peak area and peak height data for 6. Calibration curve:
        for i in Solvent.solvents:

            for j in range(4):
                self.solvent_sheets[i.name][f"I{62 + j}"] = getattr(i, "a" + f"{8 - j}")[2]
                self.solvent_sheets[i.name][f"F{62 + j}"] = getattr(i, "a" + f"{8 - j}")[0]

            for j in range(4):
                self.solvent_sheets[i.name][f"F{66 + j}"] = getattr(i, "a" + f"{4 - j}")[0]

        self.collected_messages += f"<li>Data of files <span style='color: #48dbfb;'>A1</span> to <span style='color: #48dbfb;'>A8</span> have been transferred successfully!</li>"

        self.add_area_height_data_b()

    def add_area_height_data_b(self):

        for i in Solvent.solvents:

            # Add peak area and retention time data for 7. Repeatability and control:
            for j in range(3):
                self.solvent_sheets[i.name][f"G{84 + j}"] = getattr(i, "b3_" + f"{j + 1}")[2]
                self.solvent_sheets[i.name][f"H{84 + j}"] = getattr(i, "b3_" + f"{j + 1}")[0]

            # # Add peak area for 8. Data for bracketing control:
            for j in range(5):
                try:
                    self.solvent_sheets[i.name][f"G{95 + j}"] = getattr(i, "b3_" + f"{j + 4}")[0]
                except TypeError:
                    pass

        self.collected_messages += f"<li>Data of files <span style='color: #48dbfb;'>B3.1</span> to <span style='color: #48dbfb;'>B3.4</span> have been transferred successfully!</li>"

        self.add_sample_data()

    def add_sample_data(self):

        if not len(Sample.samples) > 0:
            self.collected_messages += "<li>No sample data has been found.</li>"
            self.save_template()
            return

        if len(Sample.samples) > 5:
            self.collected_messages += "Too many samples have been submitted!"
            return

        for j in range(len(Sample.samples)):
            self.solvent_sheets[Solvent.solvents[0].name][f"A{105 + (j * 6)}"] = Sample.samples[j].sample_code

        for i in Solvent.solvents:
            for y, j in enumerate(Sample.samples):
                for z in range(3):
                    try:
                        self.solvent_sheets[i.name][f"I{105 + z + (y * 6)}"] = getattr(i, f"sample_{j.sample_code}_tag_{z + 1}")[0]
                    except TypeError:
                        pass

                try:
                    self.solvent_sheets[i.name][f"I{108 + (y * 6)}"] = getattr(i, f"sample_{j.sample_code}_tag_S_A6")[0]
                    self.solvent_sheets[i.name][f"I{109 + (y * 6)}"] = getattr(i, f"sample_{j.sample_code}_tag_S_A5")[0]
                    self.solvent_sheets[i.name][f"I{110 + (y * 6)}"] = getattr(i, f"sample_{j.sample_code}_tag_S_A4")[0]
                except TypeError:
                    pass

        self.collected_messages += f"<li>Data of <span style='color: #48dbfb;'>{len(Sample.samples)}</span> samples has been transferred successfully!</li>"

        self.save_template()

    def save_template(self):
        self.wb.save(root_dir + "/output_data/HS_Quantification Template (HH v 2.0) (processed).xlsx")
        Template.template_constructed = True
        self.collected_messages += "</ul><h1>Template is ready!</h1>"

    def return_collected_messages(self):
        return self.collected_messages

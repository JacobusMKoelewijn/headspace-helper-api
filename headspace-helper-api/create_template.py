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
import tempfile
from . import create_logger
from .config import VERSION
from .store_data import Files

log = create_logger(__name__)


class Template:
    constructed = False
    temp_output_dir = tempfile.TemporaryDirectory()

    def __init__(self, solvents, samples, diluent):
        self.wb = openpyxl.load_workbook(root_dir + "/empty_excel_template/HS_Quantification Template (HH v 2.0).xlsx")
        self.solvent_sheets = None
        self.solvents = solvents
        self.samples = samples
        self.diluent = diluent

        self.create_solvent_sheets()
        self.plot_chart()
        self.add_coa_data()
        self.add_area_height_data_a()
        self.add_area_height_data_b()
        self.add_sample_data()
        self.save_template()

    def create_solvent_sheets(self):
        """ Create a wb sheet for every solvent"""

        # Update the cell reference for each cell that has a reference in the original template:
        for j, solvent in enumerate(self.solvents):
            for cell in cells_with_reference[9:]:
                self.wb[f"solvent {j + 2}"][cell] = f"='{self.solvents[0].solvent_name}'!{cell}"

            self.wb[f"solvent {j + 1}"].title = solvent.solvent_name

        for cell in cells_with_reference[:9]:
            self.wb["Analytical Report"][cell] = f"='{self.solvents[0].solvent_name}'!{cell}"

        # Remove unused sheets if less than 12 solvents are provided.
        remaining_sheets = 13 - len(self.solvents)
        for sheet in range(remaining_sheets):
            self.wb.remove(self.wb[f"solvent {sheet + len(self.solvents) + 1}"])

        self.solvent_sheets = {solvent.solvent_name: self.wb[solvent.solvent_name] for solvent in self.solvents}

    def plot_chart(self):
        """ Generate a chart and specify the layout for all solvent sheets """

        for solvent in self.solvents:
            # Find x and y-values:
            xvalues = Reference(self.wb[solvent.solvent_name], min_col=5, min_row=62, max_row=69)
            yvalues = Reference(self.wb[solvent.solvent_name], min_col=7, min_row=62, max_row=69)

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
            self.wb[solvent.solvent_name].add_chart(chart, "N61")

    def add_coa_data(self):
        """
        Add CoA data to section: "1. Diluent", row 22.
        Add CoA data to section: "2. Reference standard", row 27.
        """

        try:
            self.solvent_sheets[self.solvents[0].solvent_name]["A22"] = self.diluent.name
            self.solvent_sheets[self.solvents[0].solvent_name]["B22"] = self.diluent.manufacturer
            self.solvent_sheets[self.solvents[0].solvent_name]["C22"] = self.diluent.catalog_number
            self.solvent_sheets[self.solvents[0].solvent_name]["D22"] = self.diluent.lot_number

        except Exception as e:
            log.info(e)

        try:
            for solvent in self.solvents:
                self.solvent_sheets[solvent.solvent_name]["A27"] = solvent.solvent_name
                self.solvent_sheets[solvent.solvent_name]["B27"] = solvent.manufacturer
                self.solvent_sheets[solvent.solvent_name]["C27"] = solvent.catalog_number
                self.solvent_sheets[solvent.solvent_name]["D27"] = solvent.lot_number
                self.solvent_sheets[solvent.solvent_name]["E27"] = solvent.purity
                self.solvent_sheets[solvent.solvent_name]["F27"] = solvent.expiration_date
                self.solvent_sheets[solvent.solvent_name]["A7"] = f"Workbook generated by Headspace Helper {VERSION}"

        except Exception as e:
            log.info(e)

    def add_area_height_data_a(self):
        """
        Add peak area and peak height to section: "6. Calibration curve", row 62 - 69.
        """

        try:
            for solvent in self.solvents:
                self.solvent_sheets[solvent.solvent_name][f"F62"] = getattr(solvent, "a8")["area"]
                self.solvent_sheets[solvent.solvent_name][f"F63"] = getattr(solvent, "a7")["area"]
                self.solvent_sheets[solvent.solvent_name][f"F64"] = getattr(solvent, "a6")["area"]
                self.solvent_sheets[solvent.solvent_name][f"F65"] = getattr(solvent, "a5")["area"]
                self.solvent_sheets[solvent.solvent_name][f"F66"] = getattr(solvent, "a4")["area"]
                self.solvent_sheets[solvent.solvent_name][f"F67"] = getattr(solvent, "a3")["area"]
                self.solvent_sheets[solvent.solvent_name][f"F68"] = getattr(solvent, "a2")["area"]
                self.solvent_sheets[solvent.solvent_name][f"F69"] = getattr(solvent, "a1")["area"]

                self.solvent_sheets[solvent.solvent_name][f"I62"] = getattr(solvent, "a8")["height"]
                self.solvent_sheets[solvent.solvent_name][f"I63"] = getattr(solvent, "a7")["height"]
                self.solvent_sheets[solvent.solvent_name][f"I64"] = getattr(solvent, "a6")["height"]
                self.solvent_sheets[solvent.solvent_name][f"I65"] = getattr(solvent, "a5")["height"]

        except Exception as e:
            log.info(e)

    def add_area_height_data_b(self):
        """
        Add peak area and peak retention time to section: "7. Repeatability and control", row 84 - 86.
        Add peak area section: "8. Bracketing control", row 95 - 99.
        """

        try:
            for solvent in self.solvents:
                self.solvent_sheets[solvent.solvent_name][f"G84"] = getattr(solvent, "b3_1")["retention time"]
                self.solvent_sheets[solvent.solvent_name][f"G85"] = getattr(solvent, "b3_2")["retention time"]
                self.solvent_sheets[solvent.solvent_name][f"G86"] = getattr(solvent, "b3_3")["retention time"]
                self.solvent_sheets[solvent.solvent_name][f"H84"] = getattr(solvent, "b3_1")["area"]
                self.solvent_sheets[solvent.solvent_name][f"H85"] = getattr(solvent, "b3_2")["area"]
                self.solvent_sheets[solvent.solvent_name][f"H86"] = getattr(solvent, "b3_3")["area"]

                self.solvent_sheets[solvent.solvent_name][f"G95"] = getattr(solvent, "b3_4")["area"]
                self.solvent_sheets[solvent.solvent_name][f"G96"] = getattr(solvent, "b3_5")["area"]
                self.solvent_sheets[solvent.solvent_name][f"G97"] = getattr(solvent, "b3_6")["area"]
                self.solvent_sheets[solvent.solvent_name][f"G98"] = getattr(solvent, "b3_7")["area"]
                self.solvent_sheets[solvent.solvent_name][f"G99"] = getattr(solvent, "b3_8")["area"]

        except Exception as e:
            log.info(e)

    def add_sample_data(self):
        """
        Add sample code and peak area for all samples in section: "9. Samples", row 105 - 134:
        """

        try:
            for j in range(len(Files.unique_sample_codes)):
                self.solvent_sheets[self.solvents[0].solvent_name][f"A{105 + (j * 6)}"] = self.samples[j].sample_code

        except Exception as e:
            log.info(e)

        try:
            for solvent in self.solvents:
                for i, sample in enumerate(self.samples):
                    self.solvent_sheets[solvent.solvent_name][f"I{105 + (i * 6)}"] = getattr(sample, solvent.solvent_name + "_tag_1")["area"]
                    self.solvent_sheets[solvent.solvent_name][f"I{106 + (i * 6)}"] = getattr(sample, solvent.solvent_name + "_tag_2")["area"]
                    self.solvent_sheets[solvent.solvent_name][f"I{107 + (i * 6)}"] = getattr(sample, solvent.solvent_name + "_tag_3")["area"]
                    self.solvent_sheets[solvent.solvent_name][f"I{108 + (i * 6)}"] = getattr(sample, solvent.solvent_name + "_tag_S_A6")["area"]
                    self.solvent_sheets[solvent.solvent_name][f"I{109 + (i * 6)}"] = getattr(sample, solvent.solvent_name + "_tag_S_A5")["area"]
                    self.solvent_sheets[solvent.solvent_name][f"I{110 + (i * 6)}"] = getattr(sample, solvent.solvent_name + "_tag_S_A4")["area"]

        except Exception as e:
            log.info(e)

    def save_template(self):
        self.wb.save(Template.temp_output_dir.name + "/HS_Quantification Template (HH v 2.0) (processed).xlsx")
        Template.constructed = True

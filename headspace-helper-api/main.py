from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
from typing import List
from . import root_dir
from os import listdir
from .core import Solvent, Diluent, Sample, Feedback
from .add_to_template import Template
import glob
import os
import tempfile
from tempfile import TemporaryDirectory
import re

app = FastAPI()

app.mount("/static", StaticFiles(directory="headspace-helper-api/static"), name="static")
templates = Jinja2Templates(directory="headspace-helper-api/templates")


def count_files(txt_files, coa_files):
    if not coa_files:
        feedback = Feedback(
            ["No CoA files provided", "Please add up to 12 solvent CoA's:", ""]
        )
        return False, feedback
    elif len(coa_files) > 12:
        feedback = Feedback(
            ["Over 12 CoA files provided", "Please add less then 12 solvent CoA's:", ""]
        )
        return False, feedback
    elif len(get_unique_samples(txt_files)) > 5:
        feedback = Feedback(
            ["Over 5 samples provided", "Please add no more then 5 samples:", ""]
        )
        return False, feedback
    else:
        return True, None


def check_file_format(txt_files, coa_files):
    """
    Check if the correct format is used for every .txt and .pdf sample. Return True if no mistakes are found. Otherwise,
    return a list of incorrect_files.
    """
    regex_sample_file = "(^[A-Z]{3}([0-9]{5}|[0-9]{8})-[0-9]{1,3}-([A-Z]|[0-9]{1,3})-([1-3]|S-A[4-6]))"
    regex_a_file = "(^A[1-8]_)"
    regex_b_file = "(^B3.[1-8]_)"
    incorrect_files = []

    for file in txt_files:
        correct_format = re.search(regex_sample_file + "|" + regex_a_file + "|" + regex_b_file, file)
        if not correct_format:
            incorrect_files.append(file)

    for file in coa_files:
        if not len(file.split()) == 6:
            incorrect_files.append(file)

    if not incorrect_files:
        return True, None
    else:
        feedback = Feedback(
            ["Incorrect file format!", "Please correct the following file names:", incorrect_files]
        )
        return False, feedback


def get_unique_samples(txt_files):
    """
    Return a set with unique sample codes extracted from all sample .txt data provided.
    """
    regex_sample_file = "^[A-Z]{3}([0-9]{5}|[0-9]{8})-[0-9]{1,3}-([A-Z]|[0-9]{1,3})"
    unique_samples = set()

    for file in txt_files:
        sample_code = re.search(regex_sample_file, file)
        if sample_code:
            unique_samples.add(sample_code.group())

    return unique_samples


def find_solvent_data(solvent_name, file_type, temp_dir):
    # don't need glob.glob?
    """
    Extract the retention time, peak area, and peak height from the data files and return as either integer or
    float for every solvent in [solvents]. Only extract the data below the '[Peak Table (Ch1)]' line and stop
    extracting once a solvent has been found. If no solvent has been found return (0,0,0).
    """

    solvent_found = False
    peak_table_found = False

    for name in glob.glob(temp_dir + "/" + f"{file_type}*.txt"):

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


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    with TemporaryDirectory() as temp_dir:
        for file in files:
            with open(temp_dir + '/' + file.filename, 'wb') as temp_file:
                shutil.copyfileobj(file.file, temp_file)

        txt_files = [os.path.basename(file) for file in glob.glob(temp_dir + "/" + "*.txt")]
        coa_files = [os.path.basename(file) for file in glob.glob(temp_dir + "/" + "*.pdf")]

        (file_count_correct, feedback) = count_files(txt_files, coa_files)
        (file_format_correct, feedback) = check_file_format(txt_files, coa_files)

        if not file_count_correct or not file_format_correct:
            return False, feedback.title, feedback.solution, feedback.information

        # Extract all required data from uploaded files and create instances of Diluent, Solvent and Sample.
        # Store extracted data as class instance attributes.

        solvents = []
        samples = []
        unique_samples = get_unique_samples(txt_files)

        # Create instances of Solvent class:
        for file in coa_files:

            solvent_name = file.split()[0]
            solvent_coa_data = file.split()

            if solvent_name in ["NMP", "DMI", "DMAC"]:
                diluent = Diluent(solvent_coa_data)
            else:
                a_file_data = {
                    f'a{i + 1}': find_solvent_data(solvent_name, "A" + f"{i + 1}", temp_dir) for i in range(12)
                }
                b_file_data = {
                    f'b3_{i + 1}': find_solvent_data(solvent_name, "B3." + f"{i + 1}", temp_dir) for i in range(8)
                }

                solvents.append(Solvent(solvent_coa_data, a_file_data, b_file_data))

        # Create instances of Sample class:
        for i, sample_code in enumerate(unique_samples):
            solvent_data = {}
            solvent_s_data = {}
            for j, file in enumerate(coa_files):
                solvent_name = file.split()[0]

                solvent_data[solvent_name] = {
                    f'tag-{i + 1}': find_solvent_data(solvent_name, f"{sample_code}-{i + 1}",
                                                       temp_dir) for i in range(3)

                }

                for i in range(3):
                    solvent_data[solvent_name][f"tag-S-A{i + 4}"] = find_solvent_data(solvent_name, f"{sample_code}-S-A{i + 4}", temp_dir)



            samples.append(Sample(sample_code, solvent_data))

    # # Add data to template.
    Template(solvents, samples, diluent)

    if Template.constructed:
        return True, "test1", "A Template has been created", ""

    # collected_messages = template.return_collected_messages()
    # feedback = "Successfull"

    # clear_all_data()

    # Remove all previous data:

    # return collected_messages, Template.template_constructed
    return True, [], [], []


@app.post("/get_template")
async def get_template(request: Request):
    print("sending")
    print(Template.temp_output_dir.name)
    # Close/remove temp_dir?
    return FileResponse(Template.temp_output_dir.name + "/HS_Quantification Template (HH v 2.0) (processed).xlsx",
                        filename="HS_Quantification Template (HH v 2.0) (processed).xlsx")

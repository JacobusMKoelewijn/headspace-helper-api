from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
from typing import List
from . import root_dir
from os import listdir
from .solvent_data import Solvent, Sample
from .add_to_template import Template
import glob
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="headspace-helper-api/static"), name="static")
templates = Jinja2Templates(directory="headspace-helper-api/templates")


def get_unique_samples():
    """
    Find all sample datafiles of format ABC12345-#-#-# or ABC12345678-#-#-# in dir
     /input_data and return a set that contains unique sample names.
    """
    all_sample_datafiles = [file for file in listdir(root_dir + "/input_data") if file[11] == "-" or file[8] == "-"]
    exclude_s_files = [file for file in all_sample_datafiles if file[file.index("_") - 4] != "S"]
    unique_samples = {file[:file.index("_") - 2] for file in exclude_s_files}
    return unique_samples


# template = Template()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    for data_file in files:
        with open(root_dir + "/input_data/" + data_file.filename, 'wb') as temp_data_file:
            shutil.copyfileobj(data_file.file, temp_data_file)

    # Create an instances of the Sample class for every unique sample and store list as class attribute.
    for i in get_unique_samples():
        # print(i)
        i = Sample(i)
        # print(i)
        Sample.samples.append(i)

    # Create an instances of the Solvent class for every solvent and store list as class attribute.
    for i in glob.glob(root_dir + "/input_data/" + "*.pdf"):
        j = Solvent(os.path.basename(i).split())
        Solvent.solvents.append(j)

    # Create a template instance:

    template.create_solvent_sheets()

    js_test = template.return_collected_messages()

    print(js_test)


    # Remove all previous data:
    files = glob.glob(root_dir + "/input_data/" + "*")
    for f in files:
        os.remove(f)

    Solvent.solvents.clear()
    Sample.samples.clear()

    # return "succes"
    return FileResponse(root_dir + "/output_data/HS_Quantification Template (HH v 1.3).xlsx", filename="HS_Quantification Tempate (HH v 1.3).xlsx")

@app.get("/upload_files")
def upload_files():
    js_test = template.return_collected_messages()
    return js_test

# @app.post("/messages")
# def messages():
#     print("being called")
#     js_test = template.return_collected_messages()
#     return js_test

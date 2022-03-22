from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
import shutil
from typing import List
import sys
from . import root_dir
from os import listdir
# from pathlib import Path
from collections import OrderedDict
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .solvent_data import Solvent, Sample
import glob
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="headspace-helper-api/static"), name="static")
templates = Jinja2Templates(directory="headspace-helper-api/templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    for data_file in files:
        with open(root_dir + "/input_data/" + data_file.filename, 'wb') as temp_data_file:
            shutil.copyfileobj(data_file.file, temp_data_file)

    collected_coa_files = [file for file in listdir(root_dir + "/input_data") if file.endswith('.pdf')]

    collected_sample_files = [file for file in listdir(root_dir + "/input_data") if file[11] == "-" or file[8] == "-"]
    unique_samples = list(OrderedDict.fromkeys([file[:file.index("_") - 2] for file in [file for file in collected_sample_files if file[file.index("_") - 4] != "S"]]))

    # print(collected_sample_files)
    # print(unique_samples)

    for name in glob.glob(root_dir + "/input_data/" + "*.pdf"):
        os.path.basename(name).split()[0] = Solvent(os.path.basename(name).split())

    for i in unique_samples:
        i = Sample(i)




    # print(collected_a_files)
    # print(collected_b_files)
    # print(collected_sample_files)
    # print(collected_coa_files)

    print("API working")
    return "succes"
    # return FileResponse(root_dir + "/output_data/HS_Quantification Template (HH v 1.4).xlsx", filename="HS_Quantification Tempate (HH v 1.4).xlsx")

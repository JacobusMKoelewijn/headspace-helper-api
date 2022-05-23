from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from tempfile import TemporaryDirectory
from .store_data import Solvent, Diluent, Sample, Files
from .config import IN_PRODUCTION, VERSION
from .create_template import Template
from . import create_logger, https_url_for
from typing import List
import shutil
import glob
import os

log = create_logger(__name__)

if IN_PRODUCTION:
    app = FastAPI(root_path="/headspace-helper")
else:
    app = FastAPI()

app.mount("/static", StaticFiles(directory="headspace-helper-api/static"), name="static")
templates = Jinja2Templates(directory="headspace-helper-api/templates")
templates.env.globals["https_url_for"] = https_url_for


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "in_production": IN_PRODUCTION,
                                                     "version": VERSION})


@app.post("/upload_files")
def upload_files(files: List[UploadFile] = File(...)):

    log.info("Creating HS_Quantification Template.xlsx worksheet")

    with TemporaryDirectory() as temp_dir:

        # Make a copy of each uploaded file in temp_dir.
        for file in files:
            with open(temp_dir + '/' + file.filename, 'wb') as temp_file:
                shutil.copyfileobj(file.file, temp_file)

        # Divide files in .txt and .pdf files.
        txt_files = [os.path.basename(file) for file in glob.glob(temp_dir + "/" + "*.txt")]
        coa_files = [os.path.basename(file) for file in glob.glob(temp_dir + "/" + "*.pdf")]

        # Create an instance of Files class.
        files = Files(txt_files, coa_files, temp_dir)

        # Check if all files meet requirements. If not return feedback to js.
        feedback = files.check_file_requirements()

        if not feedback.all_files_correct:
            return {"problem": feedback.problem,
                    "solution": feedback.solution,
                    "all_files_correct": feedback.all_files_correct,
                    "information": feedback.information
                    }

        # Store filenames as files instance attributes:
        files.set_filenames_as_attributes()

        # Store instances of solvent, diluent and sample class in data_objects dictionary:
        data_objects = {"solvent_objects": [], "sample_objects": [], "diluent_object": None}

        # Create instances of solvents and diluent:
        for file in coa_files:

            solvent_coa_data = file.split()
            solvent_name = solvent_coa_data[0]

            if solvent_name in ["NMP", "DMI", "DMA"]:
                data_objects["diluent_objects"] = Diluent(solvent_coa_data)
            else:
                data_objects["solvent_objects"].append(Solvent(solvent_coa_data, files))

        # Create instances of Samples:
        for sample_code in Files.unique_sample_codes:
            data_objects["sample_objects"].append(Sample(data_objects["solvent_objects"], sample_code, files))

    # Create an instance of Template class:
    Template(data_objects["solvent_objects"],
             data_objects["sample_objects"],
             data_objects["diluent_object"])

    if Template.constructed:
        return FileResponse(Template.temp_output_dir.name + "/HS_Quantification Template (HH v 2.0) (processed).xlsx",
                            filename="HS_Quantification Template (HH v 2.0) (processed).xlsx")

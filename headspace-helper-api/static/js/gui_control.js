'use strict';

// Panels
const titlePanel = document.querySelector('.title_panel');
const uploadPanel = document.querySelector('.upload_panel');
const uploadPanelText = document.querySelector('.upload_panel_text');
const informationPanel = document.querySelector('.information_panel');
const feedbackPanel = document.querySelector('.feedback_panel');
const feedbackPanelTitle = document.querySelector('.feedback_panel_title');
const feedbackPanelText = document.querySelector('.feedback_panel_text');

// Form
const extractData = document.querySelector('.js--extract_data');
const extractDataBtn = document.querySelector('.js--extract_data_btn');
const uploadForm = document.querySelector('#upload_form');

// Spinner
const spinner = document.querySelector('.spinner');

const panelShift = function () {
    titlePanel.style.transform = 'translateX(0px)';
    uploadPanel.style.transform = 'translateX(0px)';
    informationPanel.style.transform = 'translateX(0px)';
};

const feedbackPanelShow = function (feedback) {
    let feedbackList = '';
    feedbackPanel.style.transform = 'translateX(0px)';
    feedbackPanel.style.backgroundColor = feedback.all_files_correct ? '#78e08f' : '#e55039';
    feedbackPanelTitle.innerHTML = feedback.problem;

    try {
        for (const info of feedback.information) {
            feedbackList += `<li>${info}</li>`;
        }
    } catch (e) {
        console.error(e)
    }
    finally {
        feedbackPanelText.innerHTML = `<ul><em>${feedback.solution}</em><br><br> ${feedbackList}</ul>`;


        uploadForm.reset();
        extractDataBtn.classList.add('extract_btn_hidden');
        uploadPanelText.innerHTML =
            '<h2 class="upload_panel_text" style="margin-left: 10px; margin-top: 10px;">Upload all <span style="color: #48dbfb;">.txt</span> and <span style="color: #48dbfb;">.pdf</span> files.</h2>';
    }
};

const feedbackPanelHide = function () {
    feedbackPanel.style.transform = 'translateX(1000px)';
};


const pulsatingInput = function () {
    extractData.style.backgroundColor = '#48dbfb';
};

extractData.addEventListener('input', function (e) {
    if (extractData.files.length > 0) {
        extractDataBtn.classList.remove('extract_btn_hidden');
        extractData.classList.remove('pulse');
        extractDataBtn.classList.add('pulse');
        uploadPanelText.innerHTML =
            "Click  <span style='color: #48dbfb;'>Extract data</span>.";
    }
});

extractDataBtn.addEventListener('click', function (e) {
    feedbackPanelHide()
});

extractDataBtn.addEventListener('click', function (e) {
    spinner.classList.remove('hidden');
    extractDataBtn.classList.remove('pulse');
});

uploadForm.addEventListener('submit', e => {
    e.preventDefault();

    fetch(uploadForm.action, {
        method: 'POST',
        body: new FormData(uploadForm),
    })
        .then(response => {
        console.log(response)

        return response.blob()
        })
        .then(response => {
        console.log(response)
            if (response.type == 'application/json') {
                console.log(response);
                response.text().then(response => {
                    const json = JSON.parse(response);
                    feedbackPanelShow(json);
                    spinner.classList.add('hidden');
                });
            } else {
                const blob = new Blob([response], {
                    type: 'application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                });
                console.log(blob);
                const downloadUrl = URL.createObjectURL(blob);
                console.log(downloadUrl);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download =
                    'HS_Quantification Template (HH v 2.0) (processed).xlsx';
                document.body.appendChild(a);
                a.click();
                spinner.classList.add('hidden');
                const feedback = {
                    all_files_correct: true,
                    problem: "Success!",
                    solution: "An excel template file has been created."
                    }
                feedbackPanelShow(feedback);
            }
        })
        .catch(error => {
            console.error(error);
        });
});

window.setTimeout(panelShift, 500);
pulsatingInput();

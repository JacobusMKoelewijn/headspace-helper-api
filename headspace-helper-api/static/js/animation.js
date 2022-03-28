'use strict';

const leftPanel = document.querySelector('.left_panel');
const rightPanel = document.querySelector('.right_panel');
const leftReminder = document.querySelector('.left_reminder')
const extractData = document.querySelector('.js--extract_data');
const extractDataBtn = document.querySelector('.js--extract_data_btn');
const rightPanelText = document.querySelector('.right_panel_text');
const feedbackPanel = document.querySelector('.feedback_panel');
const uploadForm = document.querySelector('#upload_form');
const feedbackPanelText = document.querySelector('.feedback_text');
const feedbackPanelTextTitle = document.querySelector('.feedback_text_title');
const mockPanel = document.querySelector('#get_template');


const panelShift = function() {
    leftPanel.style.transform = 'translateX(0px)'
    rightPanel.style.transform = 'translateX(0px)'
    leftReminder.style.transform = 'translateX(0px)'
};

const feedbackPanelShow = function(feedback) {
    feedbackPanel.style.transform = 'translateX(0px)'
    feedbackPanelTextTitle.innerHTML = (feedback[1] ? 'Success!' : "Failed!")
    feedbackPanelText.innerHTML = `<ul>${feedback[0]}</ul>`
}

async function getTemplate() {
    console.log("submitting")
    mockPanel.submit()
}

const pulsatingInput = function() {
    extractData.style.backgroundColor = '#48dbfb'
}

extractData.addEventListener('input', function(e) {
    if (extractData.files.length > 0) {
        extractDataBtn.classList.remove('hidden');
        extractData.classList.remove('pulse')
        extractDataBtn.classList.add('pulse')
        rightPanelText.innerHTML = "Click  <span style='color: #48dbfb;'>Extract data</span>."
    }
});




uploadForm.addEventListener('submit', (e) => {
        e.preventDefault();
        fetch(uploadForm.action, {
        method: 'POST',
        body: new FormData(uploadForm),
    }).then((resp) => {
        return resp.json();
    }).then((body) => {
    console.log(body)
         feedbackPanelShow(body)
         if (body[1]) {
            getTemplate()
         }
    }).catch((error) => {
       console.error(error)
    });
});


window.setTimeout(panelShift, 500);
pulsatingInput()
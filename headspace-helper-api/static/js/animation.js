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
const feedbackPanelTextStatus = document.querySelector('.feedback_text_status')
const mockPanel = document.querySelector('#get_template');
const spinner = document.querySelector('.spinner')

const panelShift = function() {
    leftPanel.style.transform = 'translateX(0px)'
    rightPanel.style.transform = 'translateX(0px)'
    leftReminder.style.transform = 'translateX(0px)'
};

const feedbackPanelShow = function (feedback) {
  let feedbackList = ""
  feedbackPanel.style.transform = "translateX(0px)";
  feedbackPanelTextStatus.innerHTML = feedback[0] ? "Success!" : feedback[1];
  feedbackPanel.style.backgroundColor = feedback[0] ? "#78e08f" : "#e55039"

  for (const message of feedback[3]) {
    console.log(message);
    feedbackList += `<li>${message}</li>`;
  }

  feedbackPanelText.innerHTML = `<ul><em>${feedback[2]}</em><br><br> ${feedbackList}</ul>`;
};


async function getTemplate() {
    console.log("submitting")
    mockPanel.submit()
    spinner.classList.add('hidden');
}

const pulsatingInput = function() {
    extractData.style.backgroundColor = '#48dbfb'
}

extractData.addEventListener('input', function(e) {
    if (extractData.files.length > 0) {
        extractDataBtn.classList.remove('hidden2');
        extractData.classList.remove('pulse')
        extractDataBtn.classList.add('pulse')
        rightPanelText.innerHTML = "Click  <span style='color: #48dbfb;'>Extract data</span>."
    }
});

extractDataBtn.addEventListener('click', function(e) {
        spinner.classList.remove('hidden');
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
         if (body[0]) {
            getTemplate()
         } else {
            spinner.classList.add('hidden');
         }
    }).catch((error) => {
       console.error(error)
    });
});


window.setTimeout(panelShift, 500);
pulsatingInput()
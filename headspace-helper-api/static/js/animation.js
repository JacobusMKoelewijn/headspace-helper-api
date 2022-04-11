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
const feedbackPanelTitle = document.querySelector('.feedback_title')
const mockPanel = document.querySelector('#get_template');
const spinner = document.querySelector('.spinner')

const panelShift = function() {
    leftPanel.style.transform = 'translateX(0px)'
    rightPanel.style.transform = 'translateX(0px)'
    leftReminder.style.transform = 'translateX(0px)'
};

const feedbackPanelShow = function (feedback) {
    console.log(feedback)
  let feedbackList = ""
  feedbackPanel.style.transform = "translateX(0px)";
  feedbackPanelTitle.innerHTML = feedback[1].title;
  feedbackPanel.style.backgroundColor = feedback[0] ? "#78e08f" : "#e55039"

  for (const message of feedback[1].information) {
    console.log(message);
    feedbackList += `<li>${message}</li>`;
  }

  feedbackPanelText.innerHTML = `<ul><em>${feedback[1].solution}</em><br><br> ${feedbackList}</ul>`;
};

const successPanel = function() {
    feedbackPanel.style.transform = "translateX(0px)";
    feedbackPanelTitle.innerHTML = "Success!";
    feedbackPanel.style.backgroundColor = "#78e08f"
}


async function getTemplate(response) {

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
        }).then((response) => {
            return response.blob();
        }).then((response) => {

            if (response.type == "application/json") {
                console.log(response)
                response.text().then((response) => {
                    const json = JSON.parse(response)
                    feedbackPanelShow(json)
                    spinner.classList.add('hidden');
                })
            } else {
                const blob = new Blob([response], {type: 'application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
                console.log(blob)
                const downloadUrl = URL.createObjectURL(blob);
                console.log(downloadUrl)
                const a = document.createElement("a");
                a.href = downloadUrl;
                a.download = "HS_Quantification Template (HH v 2.0) (processed).xlsx";
                document.body.appendChild(a);
                a.click();
                spinner.classList.add('hidden');
                successPanel()
            }

            }).catch((error) => {
               console.error(error)
            });
});

window.setTimeout(panelShift, 500);
pulsatingInput()
'use strict';

const leftPanel = document.querySelector('.left_panel');
const rightPanel = document.querySelector('.right_panel');
const leftReminder = document.querySelector('.left_reminder')
const extractData = document.querySelector('.js--extract_data');
const extractDataBtn = document.querySelector('.js--extract_data_btn');
const rightPanelText = document.querySelector('.right_panel_text')

const panelShift = function() {
    leftPanel.style.transform = 'translateX(0px)'
    rightPanel.style.transform = 'translateX(0px)'
    leftReminder.style.transform = 'translateX(0px)'
};

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

extractDataBtn.addEventListener('click', function(e) {

    console.log("test")
});



console.log('Working');

window.setTimeout(panelShift, 500);
pulsatingInput()
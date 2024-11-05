// Switch between pages
function goToPage(pageNumber) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));

    document.getElementById(`page${pageNumber}`).classList.add('active');
}

// Initial load: show the first page
document.addEventListener('DOMContentLoaded', () => {
    goToPage(1);
});

// Validate input form on page 2
let selectedMode = null;

function selectMode(mode) {
    selectedMode = mode;

    const tensileModeBtn = document.getElementById("tensileModeBtn");
    const scannerModeBtn = document.getElementById("scannerModeBtn");

    tensileModeBtn.classList.remove("selected");
    scannerModeBtn.classList.remove("selected");

    if (selectedMode == 'tensile') {
        tensileModeBtn.classList.add("selected");
    } else if (selectedMode == 'scanner') {
        scannerModeBtn.classList.add("selected");
    }
}

function validateInput() {
    // const name = document.getElementById('name').value;
    const width = document.getElementById('width').value;
    const thinkness = document.getElementById('thinkness').value;
    const length = document.getElementById('length').value;



    if (width && length && thinkness && selectedMode) {
        goToPage(3);
    } else if (!selectedMode) {
        alert("Please select the experiment mode.");
    } else {
        alert("Please fill out all the fields.");
    }

}

function fillBlanks() {
    const specimenType = document.getElementById("specimen").value;
    const widthInput = document.getElementById("width");
    const thinkessInput = document.getElementById("thinkness");
    const lengthInput = document.getElementById("length")

    if (specimenType === "type4") {
        widthInput.value = 6;
        thinkessInput.value = 3.2;
        lengthInput.value = 25;
    } else if (specimenType === "type5") {
        widthInput.value = 3.18;
        thinkessInput.value = 3.2;
        lengthInput.value = 7.62;
    } else {
        widthInput.value = '';
        thinkessInput.value = '';
        lengthInput.value = '';
    }
}

//Page 3 Calibration



function initialPosition(adjType) {
    selectedAjd = adjType;
    fetch('/initial_adjust',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({adjType: adjType})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);  // Log the response from Flask
    })
    .catch(error => {
        console.error("Error:", error);
    });


    // if (selectedAjd == 'coarseCCW') {
    //     console.log("CoarseCCW");
    // } else if (selectedAjd == 'fineCCW') {
    //     console.log("FineCCW");
    // } else if (selectedAjd == 'fineCW') {
    //     console.log("FineCW");
    // } else if (selectedAjd == 'coarseCW') {
    //     console.log("CoarseCW");
    // }
}

function calibrate() {
    //Set the encoder and load cell value 0
}


// Experiment control logic
let experimentRunning = false;
let dataLog = [];


function startStopExperiment() {
    const button = document.getElementById('startStopBtn');
    if (experimentRunning) {
        button.textContent = 'Start Recording';
        experimentRunning = false;
        // Stop experiment and plotting logic
    } else {
        button.textContent = 'Stop Recording';
        experimentRunning = true;
        // Start experiment and plotting logic
        updatePlot();  // Start the plot update
    }
}

function stepExperiment() {
    console.log("Step experiment.");
    // Add logic for one step of tensile test
}

function continueExperiment() {
    console.log("Continue experiment.");
    // Add logic for continuous tensile test until failure
}

function saveData() {
    console.log("Data saved:", dataLog);
    // Add logic to save the data collected during the experiment
}

function clearData() {

}

// Real-time plotting (simulate with random data)
function updatePlot() {
    if (!experimentRunning) return;

    // Simulate real-time data update
    const randomStress = Math.random() * 100;
    const randomStrain = Math.random();

    // Update chart (assume using Chart.js or similar)

    setTimeout(updatePlot, 100);  // Update every 100ms
}

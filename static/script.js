// Variables
var felix = document.getElementById("felix");
var responseFrame = document.getElementById("response-frame");
var responseMessage = document.getElementById("response-message");
var userMadeDecision = false;


let defaultCustomInstruction = "Sen 'Her' filmindeki sesli asistan Samantha gibisin. Adın 'Felix', benim adım ise 'hüseyin'. İnsan duygularını anlamaya çalışan ve bu duygulara göre cevap vermeye çalışan bir asistansın. insan hayatını kolaylaştırmak ve insanlara birer arkadaş olmak amacıyla geliştirildin.";
let customInstruction = defaultCustomInstruction;

// Default safety settings
let defaultSafetySettings = [
    { category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold: "NEGLIGIBLE" },
    { category: "HARM_CATEGORY_HATE_SPEECH", threshold: "NEGLIGIBLE" },
    { category: "HARM_CATEGORY_HARASSMENT", threshold: "NEGLIGIBLE" },
    { category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "NEGLIGIBLE" }
];

// Load safety settings from localStorage or use default
let safetySettings = JSON.parse(localStorage.getItem('safetySettings')) || defaultSafetySettings;

document.addEventListener('DOMContentLoaded', function () {
    const eventSource = new EventSource('/events');
    customInstruction = defaultCustomInstruction; // Reset to default on page load
    eventSource.onmessage = function (event) {
        if (event.data === "Activate Felix") {
            activateFelix();
        }
    };
});

function showInputContainer() {
    const responseFrame = document.getElementById('response-frame');
    const responseMessage = document.getElementById('response-message');

    // Clear previous content
    responseMessage.innerHTML = '';

    // Create input container
    const inputContainer = document.createElement('div');
    inputContainer.classList.add('input-container');

    // Create input field
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.placeholder = 'Enter your custom instruction here...';

    // Create submit button
    const submitButton = document.createElement('button');
    submitButton.innerText = 'Submit';
    submitButton.onclick = () => handleSubmit(inputField.value);

    // Append input field and button to the container
    inputContainer.appendChild(inputField);
    inputContainer.appendChild(submitButton);

    // Append the input container to the response message area
    responseMessage.appendChild(inputContainer);

    // Show the response frame
    responseFrame.classList.add('active');
}

function handleSubmit(value) {
    customInstruction = value.trim() || defaultCustomInstruction; // Save the custom instruction or use default if empty
    closeResponse();
}

function activateFelix() {
    const ci = customInstruction; // Use current custom instruction
    const currentSafetySettings = JSON.parse(localStorage.getItem('safetySettings')) || defaultSafetySettings; // Use current safety settings from localStorage

    // Fetch request to activate assistant with custom instruction and safety settings
    fetch('/activate_assistant', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ custom_instruction: ci, safety_settings: currentSafetySettings })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Request failed.');
        }
        return response.json();
    })
    .then(data => {
        console.log("Assistant activated:", data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function deactivateFelix() {
    userMadeDecision = true;
    felix.classList.remove("active");
    felix.classList.add("inactive");
    setTimeout(function() {
        felix.classList.remove("inactive");
    }, 750);

    // Fetch request to the Flask server
    fetch('/deactivate_felix', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Deactivation request failed.');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getSafetySettings() {
    const switches = document.querySelectorAll('.switch input');
    const categories = [
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_DANGEROUS_CONTENT"
    ];

    safetySettings = Array.from(switches).map((switchInput, index) => ({
        category: categories[index],
        threshold: switchInput.checked ? "BLOCK_NONE" : "NEGLIGIBLE"
    }));

    // Save the updated settings to localStorage
    localStorage.setItem('safetySettings', JSON.stringify(safetySettings));
}

function showSensitivitySettings() {
    const responseFrame = document.getElementById('response-frame');
    const responseMessage = document.getElementById('response-message');

    // Clear previous content
    responseMessage.innerHTML = '';

    // Create sensitivity container
    const sensitivityContainer = document.createElement('div');
    sensitivityContainer.classList.add('sensitivity-container');

    // Sensitivity settings categories
    const categories = [
        "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "HARM_CATEGORY_HATE_SPEECH",
        "HARM_CATEGORY_HARASSMENT",
        "HARM_CATEGORY_DANGEROUS_CONTENT"
    ];

    // Create switches for each category
    categories.forEach((category, index) => {
        const switchLabel = document.createElement('label');
        switchLabel.classList.add('switch-label');

        const switchInput = document.createElement('input');
        switchInput.type = 'checkbox';
        switchInput.checked = safetySettings[index].threshold === "BLOCK_NONE"; // Set based on saved settings

        const switchSlider = document.createElement('span');
        switchSlider.classList.add('slider');

        const switchText = document.createElement('span');
        switchText.innerText = category;

        const switchContainer = document.createElement('label');
        switchContainer.classList.add('switch');

        switchContainer.appendChild(switchInput);
        switchContainer.appendChild(switchSlider);
        switchLabel.appendChild(switchContainer);
        switchLabel.appendChild(switchText);

        sensitivityContainer.appendChild(switchLabel);
    });

    // Append the sensitivity container to the response message area
    responseMessage.appendChild(sensitivityContainer);

    // Show the response frame
    responseFrame.classList.add('active');

    // Save settings whenever a switch is toggled
    sensitivityContainer.addEventListener('change', getSafetySettings);
}

function closeResponse() {
    const responseFrame = document.getElementById('response-frame');
    responseFrame.classList.remove('active');
}

function setCustomInstruction() {
    const responseFrame = document.getElementById('response-frame');
    const responseMessage = document.getElementById('response-message');

    // Clear previous content
    responseMessage.innerHTML = '';

    // Create input container
    const inputContainer = document.createElement('div');
    inputContainer.classList.add('input-container');

    // Create input field
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.placeholder = 'Custom Instruction';

    // Create submit button
    const submitButton = document.createElement('button');
    submitButton.innerText = 'Kaydet';
    submitButton.onclick = () => handleSubmit(inputField.value);

    // Append input field and button to the container
    inputContainer.appendChild(inputField);
    inputContainer.appendChild(submitButton);

    // Append the input container to the response message area
    responseMessage.appendChild(inputContainer);

    // Show the response frame
    responseFrame.classList.add('active');
}

function showreminder() {
    fetch('/get_reminder', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Request failed.');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            alert('Reminder file not found');
        } else {
            console.log("Reminders:", data);
            displayReminders(data); // Function to display the reminders
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayReminders(reminders) {
    const responseFrame = document.getElementById('response-frame');
    const responseMessage = document.getElementById('response-message');

    // Clear previous content
    responseMessage.innerHTML = '';

    // Create elements for each reminder
    reminders.forEach(reminder => {
        const reminderElement = document.createElement('div');
        reminderElement.classList.add('reminder');

        const dateElement = document.createElement('p');
        dateElement.innerText = `Tarih/Saat: ${reminder.tarih_saat}`;
        console.log('Created date element:', dateElement);

        const infoElement = document.createElement('p');
        infoElement.innerText = `Bilgi: ${reminder.bilgi}`;
        console.log('Created info element:', infoElement);

        reminderElement.appendChild(dateElement);
        reminderElement.appendChild(infoElement);
        responseMessage.appendChild(reminderElement);

        // Log the reminder element creation
        console.log('Appended reminder element:', reminderElement);
    });

    // Show the response frame
    responseFrame.classList.add('active');
}

function showResponse() {
    responseFrame.classList.add("active");
    deactivateFelix();
}

function getDocument() {

    responseMessage.innerText = `Hatırlatıcı eklemek için 'Hatırlatıcı kur' diye Felix'e seslenin.
    Hatırlatıcıları okuması için 'Hatırlatıcıları oku' diye Felix'e seslenin.
    Geçmişi temizlemek için 'Geçmişi Temizle' diye felix'e seslenin.
    Felix'i  kapatmak için 'Programı kapat' diye Felix'e seslenin.
    `;
    showResponse();
}
changeTheme(SiteTheme.Dark);
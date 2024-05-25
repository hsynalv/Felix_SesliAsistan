// Constants
const ACTIVE_TIME_MS = 5000;
const DEACTIVATION_TIME_MS = 750;

// Variables
var felix = document.getElementById("felix");
var responseFrame = document.getElementById("response-frame");
var responseMessage = document.getElementById("response-message");
var userMadeDecision = false;
var jokes = [
    'I ate a clock yesterday, it was very time-consuming.',
    'A perfectionist walked into a bar…apparently, the bar wasn’t set high enough.',
    'Employee of the month is a good example of how somebody can be both a winner and a loser at the same time.',
    'I don’t have a girlfriend, but I know a girl that would get really mad if she heard me say that.',
    'Relationships are great, but have you ever had stuffed crust pizza?',
    'The worst time to have a heart attack is during a game of charades.',
    'My therapist says I have a preoccupation with vengeance. We’ll see about that.',
    'I have a friend. He keeps trying to convince me he’s a compulsive liar, but I don’t believe him.'
];

let defaultCustomInstruction = "Sen 'Her' filmindeki sesli asistan Samantha gibisin. Adın 'Felix', benim adım ise 'hüseyin'. İnsan duygularını anlamaya çalışan ve bu duygulara göre cevap vermeye çalışan bir asistansın. insan hayatını kolaylaştırmak ve insanlara birer arkadaş olmak amacıyla geliştirildin.";
let customInstruction = defaultCustomInstruction;
// Activate felix and set timeout for awaiting a command.
document.addEventListener('DOMContentLoaded', function () {
    const eventSource = new EventSource('/events');
    customInstruction = defaultCustomInstruction; // Reset to default on page load
    eventSource.onmessage = function (event) {
        if (event.data === "Activate Felix") {
            activateFelix();
        }
    };
});

function activateFelix() {
    userMadeDecision = false;
    felix.classList.remove("inactive");
    felix.classList.add("active");

    const flaskURL = '/activate_assistant';

    fetch(flaskURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "custom_instruction" : customInstruction
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('İstek başarısız.');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Hata:', error);
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

function getWeather() {

    responseMessage.innerText = `Hatırlatıcı eklemek için 'Hatırlatıcı kur' diye Felix'e seslenin.
    Hatırlatıcıları okuması için 'Hatırlatıcıları oku' diye Felix'e seslenin.
    Geçmişi temizlemek için 'Geçmişi Temizle' diye felix'e seslenin.
    Felix'i  kapatmak için 'Programı kapat' diye Felix'e seslenin.
    `;
    showResponse();
}
function getDate() {
    var today = new Date();
    var date = (today.getMonth() + 1) + '/' + today.getDate() + '/' + today.getFullYear();
    responseMessage.innerText = "A calendar is a great investment you know; I mean, your computer even has one! Since you asked, today is " + date + ".";
    showResponse();
}
function tellJoke() {
    var index = Math.floor((Math.random() * jokes.length) - 1);
    responseMessage.innerText = jokes[index];
    showResponse();
}
function searchGoogle() {
    deactivateFelix();
    window.open("https://www.google.com/", "_blank");
}

function showInspiration() {
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

function getTime() {
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

function handleSubmit(value) {
    customInstruction = value.trim(); // Save the custom instruction
    console.log(customInstruction)
    closeResponse();
}

function closeResponse() {
    const responseFrame = document.getElementById('response-frame');
    responseFrame.classList.remove('active');
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
function closeResponse() {
    const responseFrame = document.getElementById('response-frame');
    responseFrame.classList.remove('active');
}
changeTheme(SiteTheme.Dark);

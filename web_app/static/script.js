let voices = [];

function loadVoices() {
    voices = window.speechSynthesis.getVoices();
}

window.speechSynthesis.onvoiceschanged = loadVoices;

// ==========================
// SPEAK FUNCTION
// ==========================
function speakText() {
    const text = document.getElementById("translated").innerText.trim();
    const speed = parseFloat(document.getElementById("speedControl").value);
    const selectedLang = document.getElementById("languageSelect").value;

    if (!text) return;

    if (voices.length === 0) {
        voices = window.speechSynthesis.getVoices();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = speed;

    const matchedVoice = voices.find(v =>
        v.lang.toLowerCase().startsWith(selectedLang)
    );

    if (matchedVoice) {
        utterance.voice = matchedVoice;
        utterance.lang = matchedVoice.lang;
    } else {
        utterance.lang = selectedLang;
    }

    window.speechSynthesis.cancel();

    setTimeout(() => {
        window.speechSynthesis.speak(utterance);
    }, 100);
}

// ==========================
// SPEECH INPUT (MIC)
// ==========================
function startListening() {
    const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert("Speech Recognition not supported.");
        return;
    }

    const recognition = new SpeechRecognition();
    const selectedLang = document.getElementById("languageSelect").value;

    recognition.lang = selectedLang + "-IN";
    recognition.start();

    recognition.onresult = function (event) {
        document.getElementById("inputText").value =
            event.results[0][0].transcript;

        // Auto-translate after speech input
        translateText();
    };
}

// ==========================
// UTILITY FUNCTIONS
// ==========================
function clearText() {
    document.getElementById("inputText").value = "";
    document.getElementById("translated").innerText = "";
}

function copyText() {
    const text = document.getElementById("translated").innerText;
    navigator.clipboard.writeText(text);
}

function swapLanguages() {
    const select = document.getElementById("languageSelect");
    const options = select.options;
    const currentIndex = select.selectedIndex;

    select.selectedIndex = (currentIndex + 1) % options.length;
}

function toggleTheme() {
    document.body.classList.toggle("light-mode");
}

// ==========================
// AUTO SPEAK STATE
// ==========================
const autoSpeakCheckbox = document.getElementById("autoSpeak");

// Restore checkbox state
if (localStorage.getItem("autoSpeak") === "true") {
    autoSpeakCheckbox.checked = true;
}

// Save checkbox state
autoSpeakCheckbox.addEventListener("change", function () {
    localStorage.setItem("autoSpeak", autoSpeakCheckbox.checked);
});

// ==========================
// TRANSLATE FUNCTION
// ==========================
function translateText() {
    const text = document.getElementById("inputText").value;
    const language = document.getElementById("languageSelect").value;

    if (!text.trim()) return;

    document.getElementById("loader").style.display = "block";

    fetch("/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text, language: language })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("translated").innerText = data.translated_text;
            document.getElementById("loader").style.display = "none";

            if (document.getElementById("autoSpeak").checked) {
                speakText();
            }
        });
}

// ==========================
// PAGE LOAD
// ==========================
window.addEventListener("load", function () {
    document.getElementById("loader").style.display = "none";

    const translated = document.getElementById("translated").innerText.trim();

    if (autoSpeakCheckbox.checked && translated) {
        setTimeout(() => {
            speakText();
        }, 500);
    }
});
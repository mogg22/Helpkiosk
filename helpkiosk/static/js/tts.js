const utterThis = new SpeechSynthesisUtterance()
const synth = window.speechSynthesis
let ourText = ""

function sendTTS (a){
    utterThis.text = a;
    synth.speak(utterThis);
};

const checkBrowserCompatibility = () => {
  "speechSynthesis" in window
    ? console.log("Web Speech API supported!")
    : console.log("Web Speech API not supported :-(")
}

checkBrowserCompatibility()

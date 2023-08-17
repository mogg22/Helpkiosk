const utterThis = new SpeechSynthesisUtterance()
const synth = window.speechSynthesis
let ourText = ""

function sendTTS (a){
    const ttsInterval = setInterval(() => {
        if (!synth.speaking) {
            utterThis.text = a;
            synth.speak(utterThis);
            clearInterval(ttsInterval);
        }
    }, 100);
};

const checkBrowserCompatibility = () => {
  "speechSynthesis" in window
    ? console.log("Web Speech API supported!")
    : console.log("Web Speech API not supported :-(")
}

checkBrowserCompatibility()

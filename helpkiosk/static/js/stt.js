var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent;
var diagnosticPara;
let elMenu2;
let categoryIndex2;

window.onload = function () {
    let elSttButton = document.querySelector('.stt-button');
    const isSound = sessionStorage.getItem('isSound') == 'true';
    if (isSound) {
        elSttButton.style.display = 'flex';
    } else {
        elSttButton.style.display = 'none';
    }
}

function kioskStt(result) {
    const elMenuAnchor = document.querySelectorAll('.menu-anchor');

    let noMatch = true;
    elMenuAnchor.forEach(function (v, k) {
        const menuString = v.getAttribute('data-tts').replace(/\n/g, '').split(' ').join('');
        if (menuString == result) {
            noMatch = false;
            location.href = v.href;
        }
    })

    if (!noMatch) return ;

    if (result == '결제하기') {
        noMatch = false;
        location.href = '/cart';
        return ;
    }

    if (result == '전체취소') {
        noMatch = false;
        const elClearForm = document.querySelector('#clear-cart');
        elClearForm.submit();
        return ;
    }
    
    sendTTS('해당 메뉴는 판매하지 않습니다');
}

function kioskMenuStt(result) {
    if (String(result).includes('추가')) {
        const elKioskMenuForm = document.querySelector('#kiosk-menu-form');
        elKioskMenuForm.submit();
        return ;
    }
    
    sendTTS('무슨 말인지 모르겠어요.');
}

function sendSpeech(page) {
    var recognition = new SpeechRecognition();
    var speechRecognitionList = new SpeechGrammarList();
    recognition.grammars = speechRecognitionList;
    recognition.lang = 'ko-KR';
    recognition.interimResults = false; // true: 중간 결과를 반환, false: 최종 결과만 반환
    recognition.continious = false; // true: 음성인식을 계속해서 수행, false: 음성인식을 한번만 수행
    recognition.maxAlternatives = 1;
    
    recognition.start();
    
    recognition.onresult = function(event) {
        var speechResult = event.results[0][0].transcript.toLowerCase();
        console.log('Confidence: ' + event.results[0][0].confidence);
        console.log('Speech Result: ' + speechResult);
        // if (diagnosticPara) {
        //     diagnosticPara.textContent = 'Speech received: ' + speechResult + '.';
        // }
        let result = speechResult.split(' ').join('');
        if (page == 'kiosk') {
            kioskStt(result);
        } else if (page == 'kiosk_menu') {
            kioskMenuStt(result);
        }
  }

  recognition.onaudiostart = function(event) {
      //Fired when the user agent has started to capture audio.
      console.log('SpeechRecognition.onaudiostart');
  }

  recognition.onaudioend = function(event) {
      //Fired when the user agent has finished capturing audio.
      console.log('SpeechRecognition.onaudioend');
  }

  recognition.onend = function(event) {
      //Fired when the speech recognition service has disconnected.
      console.log('SpeechRecognition.onend');
  }

  recognition.onnomatch = function(event) {
      //Fired when the speech recognition service returns a final result with no significant recognition. This may involve some degree of recognition, which doesn't meet or exceed the confidence threshold.
      console.log('SpeechRecognition.onnomatch');
  }

  recognition.onsoundstart = function(event) {
      //Fired when any sound — recognisable speech or not — has been detected.
      console.log('SpeechRecognition.onsoundstart');
  }

  recognition.onsoundend = function(event) {
      //Fired when any sound — recognisable speech or not — has stopped being detected.
      console.log('SpeechRecognition.onsoundend');
  }

  recognition.onspeechstart = function (event) {
      //Fired when sound that is recognised by the speech recognition service as speech has been detected.
      console.log('SpeechRecognition.onspeechstart');
  }
  recognition.onstart = function(event) {
      //Fired when the speech recognition service has begun listening to incoming audio with intent to recognize grammars associated with the current SpeechRecognition.
      console.log('SpeechRecognition.onstart');
  }
}
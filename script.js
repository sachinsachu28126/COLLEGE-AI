let lastAnswer = "";

async function sendMessage(){

let message =
document.getElementById("message").value;

let chat =
document.getElementById("chat-box");

chat.innerHTML +=
`<div class="user">
You: ${message}
</div>`;

chat.innerHTML +=
`<div class="bot">
Typing...
</div>`;

const response =
await fetch("/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
message:message
})
});

const data =
await response.json();

chat.lastElementChild.remove();

chat.innerHTML +=
`<div class="bot">
Bot: ${data.answer}
<br>
Confidence:
${data.confidence}
</div>`;

lastAnswer = data.answer;

document.getElementById(
"message"
).value = "";

chat.scrollTop =
chat.scrollHeight;
}

function fillQuestion(q){
document.getElementById(
"message"
).value = q;
}

function toggleMode(){
document.body.classList.toggle(
"dark"
);
}

function startVoice(){

let recognition =
new webkitSpeechRecognition();

recognition.onresult =
function(event){
document.getElementById(
"message"
).value =
event.results[0][0].transcript;
};

recognition.start();
}

function speakLast(){

let speech =
new SpeechSynthesisUtterance(
lastAnswer
);

speechSynthesis.speak(
speech
);
}
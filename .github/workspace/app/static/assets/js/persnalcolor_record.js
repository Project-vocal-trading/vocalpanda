const modalOpenButton = document.getElementById('modalOpenButton');
const modalCloseButton = document.getElementById('modalCloseButton');
const modal = document.getElementById('modalContainer');






modalOpenButton.addEventListener('click', () => {
  modal.classList.remove('hidden');

});




modalCloseButton.addEventListener('click', () => {
  modal.classList.add('hidden');

});



ddocument.addEventListener('DOMContentLoaded', function() {
  // 녹음 기능 추가
  var recordButton = document.getElementById('recordButton');
  var stopButton = document.getElementById('stopButton');
  var audioElement = document.getElementById('audioElement');

  var chunks = [];
  var mediaRecorder;

  recordButton.addEventListener('click', function() {
      navigator.mediaDevices.getUserMedia({ audio: true })
          .then(function(stream) {
              mediaRecorder = new MediaRecorder(stream);
              mediaRecorder.start();

              mediaRecorder.ondataavailable = function(e) {
                  chunks.push(e.data);
              };

              recordButton.disabled = true;
              stopButton.disabled = false;
          });
  });

  stopButton.addEventListener('click', function() {
      mediaRecorder.stop();

      mediaRecorder.onstop = function() {
          var blob = new Blob(chunks, { 'type': 'audio/ogg; codecs=opus' });
          chunks = [];
          var audioURL = URL.createObjectURL(blob);
          audioElement.src = audioURL;
      };

      recordButton.disabled = false;
      stopButton.disabled = true;
  });
});





var clickTimes = 0
// audio recording initialization
let shouldStop = true
let stopped = true
mediaRecorder = null
const downloadLink = document.getElementById('download');

var handleSuccess = function(stream) {  
    const options = {mimeType: 'video/webm;codecs=vp9'};
    const recordedChunks = [];
    mediaRecorder = new MediaRecorder(stream, options);  
    mediaRecorder.addEventListener('dataavailable', function(e) {
      if (e.data.size > 0) {
        recordedChunks.push(e.data);
      }
    });

    mediaRecorder.addEventListener('stop', function() {
      downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
      downloadLink.download = 'acetest.wav';
    });
};

// navigator.mediaDevices.getUserMedia({ audio: true, video: false })
//   .then(handleSuccess)
navigator.mediaDevices.getUserMedia({ audio: true, video: false })
  .then(handleSuccess);
$('#listeningSwitch').click(function(){
  // alert(clickTimes)
  if(clickTimes%2==0){
    mediaRecorder.start();
  	alert('started')

  }
  else{
  	shouldStop = true
  	mediaRecorder.stop();
  }
  clickTimes++
})
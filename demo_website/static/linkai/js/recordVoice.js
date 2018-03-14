// 获得csrftoken
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// console.log(csrftoken);

//Ajax call
function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
var $jq=jQuery.noConflict(true)
$jq.ajaxSetup({
    crossDomain: true, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// 配置xmlhttprequest对象
url = '/linkai/demo/voiceData'
var oReq = null
// oReq.open("POST", url, true);
// oReq.setRequestHeader("X-CSRFToken",csrftoken)
// oReq.onload = function (oEvent) {
//   // Uploaded.  
//   // console.log('done')
// };

var clickTimes = 0
// audio recording initialization
let shouldStop = true
let stopped = true
mediaRecorder = null
var bottomVolumn = 0.05
var recording = false
var liveSource = null
var levelChecker = null
const downloadLink = document.getElementById('download');

var handleSuccess = function(stream) {
  const options = {mimeType: 'video/webm;codecs=vp9'};
  recordedChunks = [];
  mediaRecorder = new MediaRecorder(stream, options);
  var audioContext = window.AudioContext || window.webkitAudioContext; //这是一个类
  var context = new audioContext(); //创建一个管理、播放声音的对象

  liveSource = context.createMediaStreamSource(stream); //将麦克风的声音输入这个对象
  levelChecker = context.createScriptProcessor(4096,1,1); //创建一个音频分析对象，采样的缓冲区大小为4096，输入和输出都是单声道
  levelChecker.connect(context.destination) 

  levelChecker.onaudioprocess = function(e) {
    var buffer = e.inputBuffer.getChannelData(0);
    var maxval = 0
    for(var i = 0;i<buffer.length;i++){
      if(maxval<buffer[i]){maxval=buffer[i]}
    }
    //一旦检测到音量大于阈值，就启动录音
    if(maxval>bottomVolumn){
      console.log('recording!')
      if(mediaRecorder.state=='inactive'){
        mediaRecorder.start()
      }
      recording = true
    }
    else{
      //检测到已经小于阈值，待阈值持续小一段时间后则可停止录音
      if(recording){
        mediaRecorder.stop()
        recording = false
      }
    }
  }

  //recorder相关设置
  mediaRecorder.addEventListener('dataavailable', function(e) {
    if (e.data.size > 0) {
      recordedChunks.push(e.data);
    }
  });


  mediaRecorder.addEventListener('stop', function() {
    // downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
    // console.log(downloadLink.href)
    // downloadLink.download = 'acetest.wav';

    // 收到后台返回结果时的处理，每一次stop都新建一个xhr对象
    oReq = new XMLHttpRequest();
    oReq.onreadystatechange = function(){
      if(oReq.readyState == 4){
        // post的收到返回结果
        resultText = oReq.responseText
        $('#emotionResult').text(resultText)
        // console.log(oReq.responseText)
      }
    }
    oReq.open("POST", url, true);
    oReq.setRequestHeader("X-CSRFToken",csrftoken)
    oReq.send(new Blob(recordedChunks))
    recordedChunks=[]
  });
};



navigator.mediaDevices.getUserMedia({ audio: true, video: false,sampleRate:16000 })
  .then(handleSuccess);

//     oReq = new XMLHttpRequest();
//     oReq.open("POST", url, true);
//     oReq.setRequestHeader("X-CSRFToken",csrftoken)
// var blob = new Blob(['abc123'], {type: 'text/plain'});
// oReq.send(blob)


// $.post(url,{csrfmiddlewaretoken:csrftoken,data:"blob"},function(data,status){
//   console.log('good');
// })

var audio = null
playing = 0
d = new Date()
$('#listeningSwitch').click(function(){
  // alert(clickTimes)
  if(clickTimes%2==0){
    //recorder 开始录音
    // mediaRecorder.start();
    //开始监听
    //liveSource.connect(levelChecker); //将该分析对象与麦克风音频进行连接

    //开始播放预先准备好的音频
    audio = document.getElementById('my_audio')
    audio.play()

    var start_time = new Date()

    playing = true
    oReq = new XMLHttpRequest();
    oReq.onreadystatechange = function(){
      if(oReq.readyState == 4){
        // post的收到返回结果
        resultText = oReq.responseText
        $('#emotionResult').text(resultText)
          console.log(oReq.responseText)
      }
    }

    interval = setInterval(function(){ 
      oReq.open("POST", url, true)
      oReq.setRequestHeader("X-CSRFToken",csrftoken)
      var end_time = new Date()
      var time_interval = (end_time-start_time)/1000
      console.log(time_interval)
      oReq.send(time_interval)
    }, 100);
    // while(playing){
    //   var end_time = d.getSeconds()
    //   var time_interval = end_time-start_time
    //   // oReq.open("POST", url, true);
    //   // oReq.setRequestHeader("X-CSRFToken",csrftoken)
    //   // oReq.send(time_interval)
    // }

  }
  else{
  	//mediaRecorder.stop();
    //liveSource.disconnect(levelChecker);

    //关闭音频播放
    audio.pause()
    clearInterval(interval)
    playing = false
    audio.currentTime = 0
  }
  clickTimes++
})
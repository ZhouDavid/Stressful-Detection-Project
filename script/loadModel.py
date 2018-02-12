#coding:utf-8
import mxnet as mx
from mxnet.gluon import HybridBlock
from mxnet.gluon.model_zoo import vision
import numpy as np
from mxnet import nd,autograd
from mxnet.io import NDArrayIter
from mxnet import gluon
from scipy.io import wavfile as wav
from scipy import signal
import wave
from os import listdir
from os.path import join
import pyglet
import time

# alexnet = vision.AlexNet(classes=8)
#alexnet.load_params('anothermodel-0000.params',mx.gpu())
player = pyglet.media.Player()
def playWav(filename):
	song = pyglet.media.load(filename)
	player.queue(song)
	player.play()

emotionDict=['netural','calm','happy','sad','angry','fearful','disgust','surprised']
alexnet = vision.AlexNet(classes=8)
alexnet.load_params('model_param',ctx=mx.gpu())
testDataDirectory = './test data/'
waveFiles = [(f,join(testDataDirectory,f)) for f in listdir(testDataDirectory)]
for file in waveFiles: 
	sample_rate,wav_data = wav.read(file[1])
	print('playing {}....'.format(file[0]))
	playWav(file[1])
	time.sleep(5)
	wav_data = wav_data.T[0]
	f,t,stft_img = signal.stft(wav_data,fs=sample_rate,nfft=1024,nperseg=1024,noverlap=512)
	abs_stft_img = np.abs(stft_img)
	abs_stft_img = nd.array(abs_stft_img[:256,:256]).reshape((1,1,256,256))
	predict = alexnet(abs_stft_img.as_in_context(mx.gpu()))
	predict = nd.softmax(predict)
	emotion = emotionDict[int(nd.argmax(predict,axis=1).asscalar())]
	print('classification result:{}'.format(emotion))
	print()





import time
import numpy as np
import pandas as pd
import tensorflow as tf
import os
import sys
import json


from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import numpy as np
from modules.emotionModel import global_predict,WaveFeatureConverter


# print('------------------global session:',sess)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def demo(request):
	return render(request,'linkai/demo.html')

def voice(request):
	result = ''
	if request.method=='POST':
		data = request.body
		# 将data变为ndarray
		data = list(data)
		# 降采样：从48k转为16k
		print(len(data))
		data = [data[i] for i in range(len(data)) if i%3==0]
		data = np.array(data)
		print(data.shape)
		converter = WaveFeatureConverter()

		# generate features
		features = converter.wav_to_features_from_wav_path('E:\\IEMOCAP_full_release\\Session1\\sentences\\wav\\Ses01F_impro01\\Ses01F_impro01_F000.wav')
		# result = model.predict(features)
		# converter = WaveFeatureConverter()
		# features = converter.wav_to_features_from_wav_array(data)
		# 	print('------------------local session',global_session)
		# 	print(emotion_model.predict(features))
		# print(features.shape)
		result = global_predict(features)
		
		return HttpResponse(result)
		# list(data)
	else:
		print('only allow post not get!!!!')
	return HttpResponse(result)
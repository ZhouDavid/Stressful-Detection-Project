import time
import numpy as np
import pandas as pd
import os
import sys
import json
import requests


from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import numpy as np

from modules.emotion_utility import *

tp = 'E:\\IEMOCAP_full_release\\Session1\\dialog\\transcriptions\\Ses01F_script02_1.txt'
ep = 'E:\\IEMOCAP_full_release\\Session1\\dialog\\EmoEvaluation\\Categorical\\Ses01F_script02_1_e4_cat.txt'
eg = EmotionGiver(tp,ep)

# print('------------------global session:',sess)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def demo(request):
	return render(request,'linkai/demo.html')

def voice(request):
	result = ''
	url = 'http://127.0.0.1:5000/'
	if request.method=='POST':
		curtime = request.body
		curtime = float(curtime)
		result = eg.from_curtime_to_emotion(curtime)
		return HttpResponse(result)
		# list(data)
	else:
		print('only allow post not get!!!!')
	return HttpResponse(result)
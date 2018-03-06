from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import numpy as np
from modules import emotionModel

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def demo(request):
	return render(request,'linkai/demo.html')

def voice(request):
	result = ''
	if request.method=='POST':
		data = request.body
		model = emotionModel.loadModel()
		result = model.predict(list(data))
		return HttpResponse(result)
		# list(data)
	else:
		print('only allow post not get!!!!')
	return HttpResponse(result)
#coding:utf-8
from os import listdir
from os.path import join
import scipy
from scipy.io import wavfile as wav
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import time
import random
from tqdm import tqdm
import struct
from PIL import Image

def isWavFile(filename):
	if filename.endswith('.wav'):
		return True
	return False

def getFileFullName(root):
	return [join(root,name) for name in listdir(root) if isWavFile(name)]

# def cutImage(img):
# 	'''
# 	cut image along y-axis from the bottom of of y,the reshaped size
# 	should be 256*256
# 	'''
# 	return img[:256,:256]


def amplifyImg(img,height,width):
	img = np.array(Image.fromarray(img).resize(size=(width,height)))
	return img

def shrinkImg(img,height,width):
	img = np.array(Image.fromarray(img).resize(size=(width,height)))
	return img

btime = time.time()
root_path = './RAVDESS-SpeechAO_AllActors/'
raw_img_list = []
cut_img_list = []
file_full_name_list = getFileFullName(root_path)

for i in tqdm(range(len(file_full_name_list))):
	file = file_full_name_list[i]
	sample_rate, wav_data = wav.read(file)  #sample rate is a number,wav_data is np.array
	wav_data = wav_data.T[0]
	label = file.split('/')[-1].split('-')[2]
	f,t,stft_img = signal.stft(wav_data,fs=sample_rate,nfft=1024,nperseg=1024,noverlap=512)
	abs_stft_img = np.abs(stft_img)
	raw_img_list.append((abs_stft_img,label))
	abs_stft_img = abs_stft_img[:256,:256]
	cut_img_list.append((abs_stft_img,label))

#np.save('cut_img_list',cut_img_list)
amplify_num = 1440
shrink_num = 1440
#amplify images
for i in random.sample(range(len(raw_img_list)),amplify_num):
	img = raw_img_list[i][0]
	label = raw_img_list[i][1]
	print(img.shape[0],img.shape[1])
	img = amplifyImg(img,int(img.shape[0]*1.41),int(img.shape[1]*1.41))
	cut_img_list.append((img[:256,:256],label))

#shrink images
for i in random.sample(range(len(raw_img_list)),shrink_num):
	img = raw_img_list[i][0]
	label = raw_img_list[i][1]
	img = shrinkImg(img,int(img.shape[0]/1.41),int(img.shape[1]/1.41))
	img = amplifyImg(img,256,256)
	cut_img_list.append((img,label))
	
print(len(cut_img_list))
np.save('cut_img_list',cut_img_list)
etime = time.time()
print(etime-btime)
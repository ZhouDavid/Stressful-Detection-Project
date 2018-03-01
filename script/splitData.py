#coding:utf-8
from os import listdir
from os.path import join
import scipy
from scipy.io import wavfile as wav
from sklearn import preprocessing
import numpy as np
import math
from scipy import signal
import tqdm

# constant definition
wave_span = 6
wave_mean = 0
wave_variance = 1
sample_rate = 16000

# data location initialization
wav_directory = '../data/'
RAVDESS_path = wav_directory+'RAVDESS-SpeechAO_AllActors'
Toronto_path = wav_directory+'Toronto'
IEMOCAP_path = 'E:/IEMOCAP_full_release/'
sessions = ['Session1','Session2','Session3','Session4','Session5']
IEMOCAP_root_list = [IEMOCAP_path+session+'/sentences/wav/' for session in sessions]
IEMOCAP_path_list = []
for root in IEMOCAP_root_list:
	dirs = listdir(root)
	for path in dirs:
		IEMOCAP_path_list.extend([root+path+'/'+file for file in listdir(root+path) if file.endswith('wav')])

datapath_list = [RAVDESS_path,Toronto_path]


def resample(data,resample_rate,original_rate):
	# data is a numpy array of wav
	resample_num = math.floor(resample_rate/original_rate*data.shape[0])
	return scipy.signal.resample(data,resample_num)

# read data
wavfile_list = IEMOCAP_path_list

# # to be deleted
# wavfile_list = wavfile_list[:20]
processed_audio_list = []
for wavfile in wavfile_list:
	try:
		rate,wav_data = wav.read(wavfile)
	except:
		print('read wavfile failed')
	# choose the first track of wav
	if len(wav_data.shape)>1:
		wav_data = wav_data.T[0]
	# standarlize raw sequence
	scaled_wav_data = preprocessing.scale(wav_data)
	
	# resample wav data
	#scaled_wav_data = resample(scaled_wav_data,sample_rate,rate)


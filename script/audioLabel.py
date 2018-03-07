# coding:utf-8
'''
本脚本要完成的功能是对IEMOCAP和ravdess两个数据集数组化，
每一个wav用一个不定长的数组表示，并配上标签
对于IEMOCAP数据，总共11个标签，label数组为['Neutral', 'Frustration', 'Other', 
'Disgust', 'Surprise', 'Excited', 'Anger', 'Fear', 'Sadness', 'Happiness', 'Overlap']
对于RAVDESS,总共8个标签，为['netural','calm','happy','sad','angry','fearful','disgust','surprised']
'''

import os
from os import listdir
from os.path import join
import scipy
from scipy.io import wavfile as wav
import matplotlib.pyplot as plt
from scipy import signal
from sklearn import preprocessing
import numpy as np
import time
import random
from tqdm import tqdm
import struct
from PIL import Image

IEMOCAP_EMOTIONS=['Neutral', 'Frustration', 'Other',\
'Disgust', 'Surprise', 'Excited', 'Anger', 'Fear', 'Sadness', 'Happiness', 'Overlap']
RAVDESS_EMOTIONS=['netural','calm','happy','sad','angry','fearful','disgust','surprised']

IEMOCAP_DIR='D:\\David Zhou\\Stressful Detection Project\\data\\Emotion Dataset\\IEMOCAP_full_release'
RAVDESS_DIR='D:\\David Zhou\\Stressful Detection Project\\data\\Emotion Dataset\\RAVDESS-SpeechAO_AllActors'

RAVDESS_TARGET_DIR = 'D:\\David Zhou\\Stressful Detection Project\\data\\preprocessed data\\RAVDESS'
def findAllFilePaths(root,suffix='.wav'):
    # give a directory and return all file's absolute paths ending with {suffix}
    wavFilePaths = list()
    queue = list()
    queue.append(root)
    while (len(queue)):
        currentDir = queue.pop(0)
        if os.path.isdir(currentDir):
            queue.extend([join(currentDir,d) for d in listdir(currentDir) if os.path.isdir(join(currentDir,d))])
            wavFilePaths.extend([join(currentDir,w) for w in listdir(currentDir) if w.endswith(suffix)])
    return wavFilePaths

def readAllWaves(paths):
	'''
	give wav absolute paths and return 
	a list of numpy array which is scaled
	'''
	scaled_wavs = list()
	for path in paths:
		sample_rate,wav_data = wav.read(path)
		scaled_wav_data = preprocessing.scale(wav_data)
		scaled_wavs.append(scaled_wav_data)
	return scaled_wavs

def readRavdessLabels(paths):
	'''
	give a list of file paths
	return a list of labels 
	corresponding to each path
	'''
	return [int(path.split('\\')[-1].split('-')[2]) for path in paths]

# 处理RAVDESS数据
ravdess_paths = findAllFilePaths(RAVDESS_DIR)
print('processing data')
ravdess_data = readAllWaves(ravdess_paths)
ravdess_labels = readRavdessLabels(ravdess_paths)

# 给每个wav array贴上标签
print('tagging')
labeled_ravdess_data = list()
for i in range(len(ravdess_labels)):
	labeled_ravdess_data.append((ravdess_data[i],ravdess_labels[i]))
print('saving')
np.save(os.path.join(RAVDESS_TARGET_DIR,'RAVDESS_SERIES.npy'),labeled_ravdess_data)


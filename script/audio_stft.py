# coding:utf-8
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

# constant definition


def isWavFile(filename):
    if filename.endswith('.wav'):
        return True
    return False


def getFileFullNames(root):
    return [join(root, name) for name in listdir(root) if isWavFile(name)]

def amplifyImg(img, height, width):
    img = np.array(Image.fromarray(img).resize(size=(width, height)))
    return img


def shrinkImg(img, height, width):
    img = np.array(Image.fromarray(img).resize(size=(width, height)))
    return img


def findAllFilePaths(root,suffix='.wav'):
    wavFilePaths = list()
    queue = list()
    queue.append(root)
    while (len(queue)):
        currentDir = queue.pop(0)
        if os.path.isdir(currentDir):
            queue.extend([join(currentDir,d) for d in listdir(currentDir) if os.path.isdir(join(currentDir,d))])
            wavFilePaths.extend([join(currentDir,w) for w in listdir(currentDir) if w.endswith(suffix)])
    return wavFilePaths

def getLabelFromFileName(filename):
    '''
    :param filename: 'wav\Ses01F_impro01\Ses01F_impro01_F000.wav'
    :return: the label of the file
    '''
    key = filename.split('\\')[-1][0:-4]
    emotion_id = -1
    e = label_dictionary[key]
    for i in range(len(emotions)):
        if emotions[i]==e:
            emotion_id = i
            return emotion_id

btime = time.time()
# root_path = './RAVDESS-SpeechAO_AllActors/'
root_path = 'D:\David Zhou\Stressful Detection Project\data\Emotion Dataset\IEMOCAP_full_release'
raw_img_list = []
cut_img_list = []
file_full_name_list = getFileFullNames(root_path)

wav_paths = findAllFilePaths(root=root_path,suffix='.wav')
cat_paths = findAllFilePaths(root=root_path,suffix='cat.txt')
label_dictionary = dict()
# read label file
for filename in cat_paths:
    file = open(filename,'r')
    records = file.readlines()
    for r in records:
        key = r.split(' ')[0]
        val = r.split(' ')[1].strip(':;')
        label_dictionary[key] = val

emotions = list(set(label_dictionary.values()))


for i in tqdm(range(len(wav_paths))):
    filename = wav_paths[i]
    try:
        sample_rate, wav_data = wav.read(filename)  # sample rate is a number,wav_data is np.array
    except:
        print('here!!!!')
    label = getLabelFromFileName(filename)
    scaled_wav_data = preprocessing.scale(wav_data)
    f, t, stft_img = signal.stft(scaled_wav_data, fs=16000, nfft=512, nperseg=512, noverlap=400)
    abs_stft_img = np.abs(stft_img)
    # print(abs_stft_img.shape)
    if abs_stft_img.shape[1]>256:
        raw_img_list.append((abs_stft_img, label))
        abs_stft_img = abs_stft_img[:256, :256]
        cut_img_list.append((abs_stft_img, label))
    # if i>100:break

print(len(raw_img_list))
amplify_num = len(cut_img_list)
shrink_num = len(cut_img_list)
# amplify images
print('amplifying images...')
for i in random.sample(range(len(raw_img_list)), amplify_num):
    img = raw_img_list[i][0]
    label = raw_img_list[i][1]
    # print(img.shape[0], img.shape[1])
    img = amplifyImg(img, int(img.shape[0] * 1.41), int(img.shape[1] * 1.41))
    cut_img_list.append((img[:256, :256], label))
    # if i>100:break

# shrink images
print('shrinking images...')
for i in random.sample(range(len(raw_img_list)), shrink_num):
    img = raw_img_list[i][0]
    label = raw_img_list[i][1]
    img = shrinkImg(img, int(img.shape[0] / 1.41), int(img.shape[1] / 1.41))
    img = amplifyImg(img, 256, 256)
    cut_img_list.append((img, label))
    # if i>100:break

print(len(cut_img_list))
split_points = np.linspace(0,len(cut_img_list),num=4)
for i in range(len(split_points)):
    if i < len(split_points)-1:
        print('saving image {}...'.format(str(i)))
        start = int(split_points[i])
        end = int(split_points[i+1])
        print(start,end)
        np.save('IEMOCAP_STFT_IMAGE'+str(i), cut_img_list[start:end])

etime = time.time()
print(etime - btime)
import time
import numpy as np
import pandas as pd
import tensorflow as tf
import os
import sys
import json

from sklearn.preprocessing import label_binarize
from sklearn.cross_validation import StratifiedKFold, KFold, train_test_split

import keras.backend as K
from keras.models import Sequential, Model, model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import Merge
from keras.layers import LSTM, Input, Lambda
from keras.layers.wrappers import TimeDistributed
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD, Adam, RMSprop
from keras.models import load_model

from utilities.utils import *
from utilities.calculate_features import calculate_features

from scipy.io import wavfile as wav

class CTCEmotionModel():
	def __init__(self,session,model_path='ctc_emotion_model.h5'):
		self.model = None
		self.model_path = model_path
		self.load_emotion_model(model_path)
		# 初始化session，为tf构建环境
		self.session = session
		self.emotions = np.array(['angry', 'exciting', 'neutural', 'sad'])


	def load_emotion_model(self,model_path):
		# load keras model
		overall_model = load_model(model_path,custom_objects={'<lambda>': lambda y_true, y_pred: y_pred})
		# 原始model的输出并不是我们真正想要的输出，原始的输出是loss，我们需要从原始model中抽出output层，要那个输出
		self.model = Model(inputs = overall_model.input,outputs=overall_model.get_layer('time_distributed_4').output)

	def predict(self,features):
		# data应该是一个sequence,shape=1*n*34
		# 构造input_data
		input_sequence_length = features.shape[0]
		# pad features to fix length which is 78
		# pad_sequence_into_array 认为input应该是一个utterance数组的features,所以这里需要在外面再套一层
		input_features,input_mask = pad_sequence_into_array(np.array([features]), maxlen=78)
		# print(input_features.shape)

		input_data = {'the_input':input_features,'the_labels':np.array([0]),
				'input_length':np.array([input_sequence_length]),
				'label_length':np.array([1])
				}
		with self.session.as_default():
			pred = self.model.predict(input_data)
		decode_function = K.ctc_decode(pred[:,2:,:], input_data["input_length"]-2, greedy=False, top_paths=1)
		emotion_result_id = decode_function[0][0].eval(session=tf.Session())[0][0]
		emotion_result = self.emotions[emotion_result_id]
		return emotion_result

class WaveFeatureConverter():
	def wav_to_features_from_wav_path(self,wav_path):
		'''
		read wav_path 然后将原始wav数组转化为feature向量sequence
		设sequence长度为n,则返回的features的shape=n*34，34是选取特征的个数
		'''
		try:
			# frames必须是单通道的！！！也就是说len(frames.shape)==1
			sample_rate,frames = wav.read(wav_path)
			print(frames.shape)

			if len(frames.shape)!=1:
				# converting
				frames = frames.T[0]
				print('frames must be single track audio array')
		except:
			print('path cannot be read')
			sys.exit(-1)
		raw_features = calculate_features(frames, freq=48000,options=None).T
		# 筛掉过小的feature line
		features = [f for f in raw_features if f[1]>1e-4]
		features = np.array(features,dtype=float)
		return features

	def wav_to_features_from_wav_array(self,frames):
		# wav_array should be a ndarray
		raw_features = calculate_features(frames, freq=16000,options=None).T
		# 筛掉过小的feature line
		features = [f for f in raw_features if f[1]>1e-4]
		features = np.array(features,dtype=float)
		print(features.shape)
		return features

# 初始化emotion model
global_session = tf.Session()
with global_session.as_default():
	emotion_model = CTCEmotionModel(global_session)

def global_predict(features):
	return emotion_model.predict(features)
		


# if __name__ == '__main__':
# 	global_session = tf.Session()
# 	with global_session.as_default():
# 		model = CTCEmotionModel(global_session)

# 	converter = WaveFeatureConverter()
# 	# read input data,now features still have various lengths
# 	features = converter.wav_to_features_from_wav_path('C:\\Users\\ZhouJianyu\\Desktop\\Stressful-Detection-Project\data\\RAVDESS-SpeechAO_AllActors\\03-01-04-01-01-02-11.wav')
# 	# wav = np.linspace(-1000*np.pi, 1000*np.pi, 40000)
# 	# features = converter.wav_to_features_from_wav_path('C:\\Users\\ZhouJianyu\\Desktop\\Stressful-Detection-Project\\data\\Toronto\\OAF_bar_angry.wav')
# 	# features = wav_to_features_from_wav_array(np.sin(wav))
	
# 	with global_session.as_default():
# 		print(model.predict(features))


# 我也不知道为啥，反正就是得在网站刚启动的时候让model先predict一次才能正常工作
converter = WaveFeatureConverter()
features = converter.wav_to_features_from_wav_path('E:\\IEMOCAP_full_release\\Session1\\sentences\\wav\\Ses01F_impro01\\Ses01F_impro01_F000.wav')
print(global_predict(features))
# print(features.shape)
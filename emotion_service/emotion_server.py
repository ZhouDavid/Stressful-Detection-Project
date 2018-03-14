import sys
import time

from flask import Flask, request, jsonify

import tensorflow as tf
from emotionModel import CTCEmotionModel,WaveFeatureConverter,global_predict

app = Flask(__name__)

# model initialization
global_session = tf.Session()
converter = WaveFeatureConverter()

with global_session.as_default():
	emotion_model = CTCEmotionModel(global_session)


@app.route("/", methods=['POST'])
def emotion_classify():
	data = request.json['data']
	emotion = 'silent'
	eatures = converter.wav_to_features_from_wav_array(data)
	# except:
	# 	print('----------------------encouter error when calculate features----------')
	# try:
	s = time.time()
	emotion = global_predict(features)
	e =time.time()
	print(e-s)
	print('success!!!!!!!!!emotion is {}'.format(emotion))
	# except:
	# 	print('----------------------encouter error when predicting------------------')
	return emotion

app.run(host='0.0.0.0', port=5000)
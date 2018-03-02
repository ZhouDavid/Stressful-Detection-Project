# coding:utf-8
from flask import Flask, request, jsonify
from flask import render_template
from flask import url_for

app = Flask(__name__)
# Tell `app` that if someone asks for `/` (which is the main page)
# then run this function, and send back the return value
@app.route("/",methods=['GET'])
def classify(name=None):
	return render_template('home.html')


app.run(host='0.0.0.0', port=8888)
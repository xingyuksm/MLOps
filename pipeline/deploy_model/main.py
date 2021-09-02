from fastapi import FastAPI, Request
import numpy as np
import xgboost
from sklearn import preprocessing
import os
import pathlib
import pickle
import argparse
import logging

app = FastAPI()

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s : %(lineno)d] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

# Set path to files as ENV vars in Docker file or Docker run command
model_file_path = os.getenv('MODEL_FILE_PATH')
label_encoder_path = os.getenv('LABEL_ENCODER_PATH')

@app.get("/")
def read_root():
    return {"API": "Running", "Version": "1.0"}

@app.post("/predict")
def predict(
	speal_length: float, 
	sepal_width: float, 
	petal_length: float, 
	pental_width: float):
    values = preprocess(speal_length, sepal_width, petal_length, pental_width)
    result = inference(values, model_file_path, label_encoder_path)
    return {"Results": result}

#################### Model Function ##############

MODEL = None
LE = None

def load_model(model_file_path):
	'''Load saved model by input model_file_path

	'''
	p = pathlib.Path(model_file_path)
	if not p.exists():
		logger.error(f"Model file does not exist at {model_file_path}.")
	return pickle.load(open(p, 'rb'))

def load_le(label_encoder_path):
	p = pathlib.Path(label_encoder_path)
	if not p.exists():
		logger.error(f"Label encoder does not exist at {label_encoder_path}")
	return pickle.load(open(p, 'rb'))

def preprocess(speal_length, sepal_width, petal_length, pental_width):
	values = np.array([speal_length, sepal_width, petal_length, pental_width])

	return values.reshape(-1, 4)

def inference(input_data, model_file_path, label_encoder_path):
	'''Get predictions for input data.

	'''
	global MODEL
	global LE

	if not MODEL:
		MODEL = load_model(model_file_path)
	if not LE:
		LE = load_le(label_encoder_path)

	assert input_data.shape[1] == 4

	result = MODEL.predict(input_data)
	result = LE.inverse_transform(result)
	return result.tolist()
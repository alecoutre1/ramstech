from utils.nn_models import load_kapre_model

import numpy as np
import settings
import flask
import uuid
import os
import librosa
import json
import pydub

import soundfile as sf
from evaluation.evaluation import mean_song_output
import tensorflow as tf
from flask import jsonify

import subprocess
import logging
from logging.handlers import RotatingFileHandler
import argparse
BASE_DIR = os.path.dirname(os.path.abspath(__file__))



# ARGUMENT PARSING

ap = argparse.ArgumentParser(description='Script to launch the app')

ap.add_argument("-m", "--model", required=False,default='model', help="Path to the model folder")
ap.add_argument("-ll", "--log_level", required=False,default='INFO', choices=['ERROR','WARNING','INFO','DEBUG'], help="Set log verbosity")

args = vars(ap.parse_args())

# LOG CONFIG

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = RotatingFileHandler('logs/{}'.format(__file__.replace('.py','.log')),mode='w',maxBytes=10*1024*1024, backupCount=5)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()

if args.get('log_level'):
    loglevel = args.get('log_level')

    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    ch.setLevel(numeric_level)
else :
    ch.setLevel(logging.INFO)



# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


# initialize our Flask application
app = flask.Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# LOAD DATA

def load_model_data(dir_path):
    names = json.load(open(os.path.join(dir_path, 'names.json')))
    model = load_kapre_model(os.path.join(dir_path, 'model.h5'))
    graph = tf.get_default_graph()
    return {'model': model, 'names': names,'graph':graph}

model_path = args.get('model')

model_data = load_model_data(model_path)

logging.info("Model loaded")


INDICES = json.load(open(os.path.join(model_path,'indices.json'),'r'))
logger.debug('Indices loaded')


logger.info("Starting web service...")

@app.route("/")
def homepage():
    return "Welcome to the Ramstech REST API!"


@app.route("/predict", methods=["POST"])
def predict():

    data = {"success": False}
    try:
        if flask.request.method == "POST":
            logger.info("New request")
            src = load_src_from_request(flask.request)

            if src.shape[0] < settings.MUSIC_SAMPLE_RATE* settings.MUSIC_MIN_LENGTH:
                raise Exception('ERR_TOO_SHORT_FILE')

            if src.shape[0] > settings.MUSIC_SAMPLE_RATE* settings.MUSIC_MAX_LENGTH:
                raise Exception('ERR_TOO_LONG_FILE')


            if flask.request.form.get('seuil_pred'):
                seuil_prediction = float(flask.request.form.get('seuil_pred'))
                if seuil_prediction > 1 or seuil_prediction < 0:
                    seuil_prediction = 0.05
            else:
                seuil_prediction = 0.05

            logger.info(flask.request.form)

            preds = {}
            with (model_data['graph']).as_default():
                outs = mean_song_output(model_data['model'], src)

            for k in INDICES:
                inds = INDICES[k]
                sort_by_arg =flask.request.form.get('sort_by')

                outs_k = outs[inds]
                names_k = [model_data['names'][i] for i in inds]

                if sort_by_arg =='probability':
                    list_probs = sorted(zip(names_k, outs_k), reverse=True, key=lambda t: t[1])
                elif  sort_by_arg =='name':
                    list_probs = sorted(zip(names_k, outs_k), key=lambda t: t[0].lower())
                else:
                    list_probs = zip(names_k, outs_k)
                output = []
                for (label, out) in list_probs:
                    r = {"indexation": label, "probability": float(out)}
                    if r['probability']>seuil_prediction:
                         output.append(r)
                preds.update({k: output})

            data["predictions"] = preds

            data["success"] = True

        else:
            raise Exception('ERR_NOT_POST')
    except Exception as e:
        data["ERR_MESSAGE"] = str(e)
        logger.exception(str(e))

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



def fast_load_mp3(path):
    wav_path = os.path.join(BASE_DIR, 'tmp/mp3','audio.wav')

    sound = pydub.AudioSegment.from_mp3(path)

    if (sound.duration_seconds > settings.MUSIC_MAX_LENGTH):
        raise Exception('ERR_TOO_LONG_FILE')
    if (sound.duration_seconds < settings.MUSIC_MIN_LENGTH):
        raise Exception('ERR_TOO_SHORT_FILE')


    temp_path = os.path.join(BASE_DIR, 'tmp/mp3','temp.wav')
    sound.export(temp_path, format="wav")

    process = subprocess.Popen("sox "+temp_path+' '+wav_path+' rate'+' 12000 ', shell=True, stdout=subprocess.PIPE)
    process.wait()

    src, sr = sf.read(wav_path, dtype='float32')
    if len(src.shape)==2:
        src =  np.swapaxes(src,0,1)
    src = librosa.to_mono(src)

    os.remove(temp_path)
    os.remove(wav_path)


    return src





def load_src_from_request(request):
    if request.files.get("file"):
        file = flask.request.files['file']
        format = file.filename.split('.')[-1]

        if format not in settings.MUSIC_ALLOWED_FORMATS:
            raise Exception('ERR_INCORRECT_FILE_FORMAT')

        k = str(uuid.uuid4()) + '.mp3'

        path = os.path.join(BASE_DIR, 'tmp/mp3', k)
        file.save(path)

        src = fast_load_mp3(path)
        os.remove(path)
    else:
        raise Exception('ERR_INCORRECT_ARGUMENT')

    return src



if __name__ == "__main__":
    app.run(port=4444)

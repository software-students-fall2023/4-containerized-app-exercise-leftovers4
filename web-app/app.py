from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    session,
)

import pymongo
import re
from bson.objectid import ObjectId
from pymongo import MongoClient
import os
from db import db
from bson import json_util
from bson import Binary
import json
from audio import record_audio
from gridfs import GridFS
from gridfs import GridFSBucket
import random


def parse_json(data):
    return json.loads(json_util.dumps(data))

# audioFiles = db[os.getenv("MONGODB_COLLECTION")]

# connecting to database
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("MONGODB_DATABASE")]
collection = db[os.getenv("MONGODB_COLLECTION")]

app = Flask(__name__)


# index route (redirects to /home)
@app.route("/")
def index():
    # return render_template('/index.html', flask_test='This test is a success!')
    return redirect(url_for("home"))

# /home route: passes a 'countdown' var, and 'title' for header
@app.route('/home')
def home():
    duration = 10
    return render_template('home.html', countdown = duration, title="Home")

# starts recording through 'record_audio' function in 'audio.py' and saves to current directory (web_app folder)
# current recording duration is 10 seconds
# database --> opens .wav file, converts to binary, and adds to database
@app.route('/start-recording', methods=['POST'])
def start_recording():
    cwd = os.getcwd()
    rand_num = random.randint(1, 100)
    file_name = 'output' + str(rand_num) + '.wav'
    curr_dirr = cwd + '/audio_files/' + file_name
    duration = 10
    record_audio(curr_dirr, duration=duration+1) 
    
    with open(curr_dirr, 'rb') as file:
        audio_data = Binary(file.read())
        
    audio_document = {
        "name": file_name,
        "audio_data": audio_data
    }
    collection.insert_one(audio_document)
    
    ## grid fs (?)
    # file_id = db.put(audio_data, filename="audiofile2.wav")
    # audio_file = fs.get(file_id)
    
    return render_template('home.html', title="Home")

if __name__ == '__main__':
    app.run(debug=True)
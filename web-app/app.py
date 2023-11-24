"""app.py

    """
import os
import random
from pymongo import MongoClient
from bson import Binary
from audio import record_audio

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
)

# connecting to database
client = MongoClient(os.getenv("MONGODB_URI"))
database = client[os.getenv("MONGODB_DATABASE")]
collection = database[os.getenv("MONGODB_COLLECTION")]

app = Flask(__name__)


@app.route("/")
def index():
    """Index route

    Returns:
        redirect: index route (redirects to /home)
    """
    return redirect(url_for("home"))


# /home route: passes a 'countdown' var, and 'title' for header
@app.route("/home")
def home():
    """Home route

    Returns:
        render_template: Home route
    """
    duration = 10
    return render_template("home.html", countdown=duration, title="Home")


@app.route("/start-recording", methods=["POST"])
def start_recording():
    """Records and adds files to database

    Returns:
        render_template: Records and adds wav binary files to database
    """
    cwd = os.getcwd()
    rand_num = random.randint(1, 100)
    file_name = "output" + str(rand_num) + ".wav"
    curr_dirr = cwd + "/audio_files/" + file_name
    duration = 10
    record_audio(curr_dirr, duration=duration + 1)

    with open(curr_dirr, "rb") as file:
        audio_data = Binary(file.read())

    audio_document = {"name": file_name, "audio_data": audio_data}
    collection.insert_one(audio_document)

    ## grid fs (?)
    # file_id = db.put(audio_data, filename="audiofile2.wav")
    # audio_file = fs.get(file_id)
    return render_template("home.html", title="Home")


if __name__ == "__main__":
    app.run(debug=True)

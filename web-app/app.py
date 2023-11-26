"""app.py

    """
import subprocess
import os
from pymongo import MongoClient
from bson import Binary
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
)
from datetime import datetime

# connecting to database
client = MongoClient(os.getenv("MONGODB_URI"))
database = client[os.getenv("MONGODB_DATABASE")]
collection = database[os.getenv("MONGODB_COLLECTION")]

app = Flask(__name__)


def convert_to_wav(input_data):
    """
    Converts an audio file to WAV format using FFmpeg.

    Parameters:
    input_data (bytes): The input audio data.
    input_format (str): The format of the input audio data.

    Returns:
    bytes: The converted audio data in WAV format.
    """
    with open("temp_input_file", "wb") as temp_input:
        temp_input.write(input_data)

    output_file = "temp_output_file.wav"
    command = [
        "ffmpeg",
        "-i",
        "temp_input_file",
        "-ar",
        "44100",
        "-ac",
        "2",
        output_file,
    ]
    try:
        subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
    except subprocess.CalledProcessError as e:
        print("An error occurred while converting the file: ", e)
        return None

    with open(output_file, "rb") as wav_output:
        wav_data = wav_output.read()

    os.remove("temp_input_file")
    os.remove(output_file)
    return wav_data


@app.route("/")
def index():
    """Index route"""
    return redirect(url_for("home"))


@app.route("/home")
def home():
    """Home route"""
    duration = 10
    return render_template("home.html", countdown=duration, title="Home")


@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """Uploads and adds audio file to database"""
    if "audioFile" in request.files:
        audio_file = request.files["audioFile"]
        audio_data = audio_file.read()
        # Convert to WAV using FFmpeg
        wav_data = convert_to_wav(audio_data)

        # Store as binary
        audio_document = {"name": audio_file.filename, "audio_data": Binary(wav_data), "recorded_date": datetime.utcnow().strftime("%B %d %H:%M:%S")}
        collection.insert_one(audio_document)
        return "Audio uploaded successfully", 200
    return "No audio file found", 400


@app.route("/results")
def results():
    """Results route
    Returns:
        render_template: Database results
    """
    audio_results = collection.find().sort("_id", -1).limit(20)
    return render_template("results.html", title="Results", audio_results=audio_results)


if __name__ == "__main__":
    app.run(debug=True)

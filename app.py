from flask import Flask, render_template, request
import subprocess
from time import sleep
import datetime

subprocess.run(["ls", "-l"]) 
# importing libraries 
import speech_recognition as sr 
import os 

# create a speech recognition object
r = sr.Recognizer()

# a function to recognize speech in the audio file
# so that we don't repeat ourselves in in other functions
def transcribe_audio(path,language):
    # use the audio file as the audio source
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        text = r.recognize_google(audio_listened, language=language)
        print(text)
    return text

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        myname="./static/"+str(int(datetime.datetime.utcnow().timestamp()))+".mp3"
        myothername=myname.replace("mp3","wav")


        cmd=subprocess.Popen(["timeout", "20s", "wget", request.form["radioflux"], "-O", myname]) 
        cmd.communicate()
        cmd1=subprocess.Popen(["ffmpeg","-i", myname, myothername]) 
        cmd1.communicate()
        message=transcribe_audio(myothername, request.form["locale"])
        return render_template("hi.html", message=message)
    else:
        return render_template("hey.html")
if __name__ == '__main__':
    app.run()

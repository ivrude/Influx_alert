"""Flask app to start and stop alarm"""
from flask import Flask, render_template
import pygame

app = Flask(__name__)


# to start musick
def play_music(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# to stop musick
def stop_music():
    pygame.mixer.music.stop()

#start alarm №1
@app.route("/webhook1", methods=["POST", "GET"])
def webhook():
    file_path = "sound/Try.mp3"
    play_music(file_path)
    return "Music started!"

#start alarm №2
@app.route("/webhook2", methods=["POST", "GET"])
def webhook22():
    file_path = "sound/fallout_4_01_Fallout_4_Main_Theme.mp3"
    play_music(file_path)
    return "Music started_22!"

# to make pdf screenshots
@app.route("/print", methods=["POST", "GET"])
def make_pdf():
    return render_template("make_pdf.html")

#to stop alarm
@app.route("/stop", methods=["POST", "GET", "OPTIONS"])
def stop():
    stop_music()
    return """
        <script>
            window.close();
        </script>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

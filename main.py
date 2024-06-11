from flask import Flask, request
import pygame

app = Flask(__name__)

def play_music(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    file_path = "Try.mp3"
    play_music(file_path)
    return 'Music started!'

@app.route('/stop', methods=['POST','GET','OPTIONS'])
def stop():
    stop_music()
    return 'Music stopped!'

if __name__ == '__main__':
    app.run(host='192.168.0.58', port=5002, debug=True)
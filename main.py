from flask import Flask, request
import pygame

app = Flask(__name__)

def play_music(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

@app.route('/webhook', methods=['POST'])
def webhook():
    file_path = "Try.mp3"
    play_music(file_path)
    return 'Music started!'

if __name__ == '__main__':
    app.run(host='192.168.0.15', port=5001, debug=True)
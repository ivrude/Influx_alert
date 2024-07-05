from flask import Flask, request
import pygame

app = Flask(__name__)

#app for alarms webhooks
def play_music(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

@app.route('/webhook1', methods=['POST','GET'])
def webhook():
    file_path = "sound/Try.mp3"
    play_music(file_path)
    return 'Music started!'

@app.route('/webhook2', methods=['POST','GET'])
def webhook22():
    file_path = "sound/fallout_4_01 Fallout 4 Main Theme.mp3"
    play_music(file_path)
    return 'Music started_22!'

@app.route('/stop', methods=['POST','GET','OPTIONS'])
def stop():
    stop_music()
    return '''
        <script>
            window.close();
        </script>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
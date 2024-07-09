from flask import Flask, Response
import cv2
import time

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture('')
    while True:

        success, frame = camera.read()
        if not success:
            print("Failed to grab frame, retrying...")
            camera.release()
            camera = cv2.VideoCapture('rtsp://admin:s0321bzd@77.47.130.226:554')
            time.sleep(1)
            continue

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        if not ret:
            print("Failed to encode frame, retrying...")
            time.sleep(1)
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.11)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

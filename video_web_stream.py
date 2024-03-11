from flask import Flask, render_template, Response, jsonify
import cv2
import time

# Stackoverflow links
# https://stackoverflow.com/questions/74515443/video-streaming-with-opencv-and-flask
# https://stackoverflow.com/questions/63362371/how-to-stop-a-flask-video-streamer


app = Flask(__name__)

class Camera():
    
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.start_time = time.time() 
        #self.stop_time  = self.start_time + 5
        self.is_decoded = False  # keep it to send it with AJAX
        
    def __del__(self):
        self.video.release()
        
    def get_feed(self):
        while(True):
            
            ret, frame = self.video.read()
            if not ret:
                break
            else:
                ret, jpeg = cv2.imencode('.jpg', frame)
                frame = jpeg.tobytes()
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
                

camera = Camera()
  

@app.route('/video_feed/')
def video_feed():
    return Response(camera.get_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
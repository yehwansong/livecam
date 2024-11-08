from flask import Flask, Response
import cv2

app = Flask(__name__)

def generate_frames():
    # Initialize the webcam
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("Could not start the camera.")

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Yield the frame as a byte stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def video_feed():
    # Video streaming route
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Run the Flask app on the local IP and port 8080
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify  ,Response
import os
from ultralytics import YOLO
import cv2
from werkzeug.utils import secure_filename
import mimetypes
import subprocess
import random




app = Flask(__name__)

# Folder for uploaded images and results
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER


app.secret_key = 'supersecretkey'

# In-memory user database (For demonstration purposes only)
users = {}

# Load YOLO model
model = YOLO(r'../runs/detect/train3/weights/best.pt')




@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('sign-in.html')

@app.route("/sigin", methods=['POST', 'GET'])
def login_data():
    if request.method == "POST":
        email = request.form["email"]
        pswd = request.form["password"]
        if email == "admin" and pswd == "admin":
            return render_template("home.html")
    return render_template('sign-in.html')

@app.route("/home")
def home():
    return render_template('home.html')






@app.route("/result")
def result():
    return render_template('image.html')

@app.route("/video")
def video():
    return render_template('video.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('home'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Video formats
            result_video_path = process_video(file_path, filename)
            return render_template('image.html', 
                                   original_file=filename, 
                                   result_video=result_video_path)

        else:  # Image file
            results = model(file_path)
            result_img_path = os.path.join(app.config['RESULTS_FOLDER'], f"result_{filename}")
            annotated_frame = results[0].plot()
            cv2.imwrite(result_img_path, annotated_frame)
            return render_template('image.html', 
                                   original_file=filename, 
                                   result_file=f"result_{filename}")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

@app.route('/results/videos/<filename>')
def result_video(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename, mimetype='video/mp4')



def process_video(input_path, filename):
    # OpenCV Video Capture
    cap = cv2.VideoCapture(input_path)
    output_path = os.path.join(app.config['RESULTS_FOLDER'], f"result_{filename}")

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)

    # Temporary file for processed frames
    temp_output = os.path.join(app.config['RESULTS_FOLDER'], "temp_video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Temporary OpenCV video
    out = cv2.VideoWriter(temp_output, fourcc, fps, frame_size)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # YOLO Processing: Annotate the frame with detections
        results = model(frame)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

    cap.release()
    out.release()

    # FFmpeg Encoding for Final Output
    ffmpeg_command = [
        "ffmpeg", "-y",  # Overwrite output if exists
        "-i", temp_output,   # Input temporary video
        "-c:v", "libx264",   # H.264 codec for encoding
        "-preset", "medium", # Encoding speed
        "-crf", "23",        # Quality (Lower is better)
        "-c:a", "aac",       # Audio codec
        "-strict", "experimental",
        output_path          # Final output video
    ]

    try:
        # Run FFmpeg to re-encode
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e}")
        raise

    # Remove temporary file
    os.remove(temp_output)

    return f"result_{filename}"  # Return relative path














# Global variable to control the video feed
camera = None

def generate_frames():
    global camera
    camera = cv2.VideoCapture(0)  # Open the default camera

    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Perform YOLO detection
        results = model.predict(frame, verbose=False)

        # Annotate detections
        for result in results[0].boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = result
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))  # Bounding box coordinates
            label = f"{model.names[int(cls)]} {conf:.2f}"  # Label with confidence

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield frame to browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/close_camera', methods=['POST'])
def close_camera():
    global camera
    if camera:
        camera.release()
        camera = None
    return '', 204

@app.route('/camera')
def camera_page():
    return render_template('camera.html')  # Ensure your HTML file is named correctly



@app.route("/performance")
def performance():
    return render_template("performance.html")

@app.route("/charts")
def charts():
    return render_template('charts.html')

@app.route("/logout")
def logout():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
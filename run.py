from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response
import os
from ultralytics import YOLO
import cv2
from werkzeug.utils import secure_filename
import serial
import time

app = Flask(__name__)

# ====== Configurations ======
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.secret_key = 'supersecretkey'

# In-memory user database (For demonstration purposes only)
users = {}

# Load YOLO model
model = YOLO(r'../runs/detect/train3/weights/best.pt')

# ====== Arduino Serial Communication ======
ser = None

def open_serial_port():
    """Open serial port connection."""
    global ser
    if ser is None or not ser.is_open:
        try:
            ser = serial.Serial('COM4', 9600, timeout=1)  # Adjust COM port if needed
            print("✅ Serial port opened:", ser.portstr)
        except serial.SerialException as e:
            print("❌ Error opening serial port:", e)
            ser = None

def close_serial_port():
    """Close serial port connection."""
    global ser
    if ser and ser.is_open:
        ser.close()
        print("🔌 Serial port closed.")

# Open serial port at app start
open_serial_port()

# Stage-to-Signal Mapping
signals = {
    'Bud': '1',
    'Flower': '2',
    'Early-Fruit': '3',
    'Mid-Growth': '4',
    'Ripe': '5'
}

def send_stage_signal(stage):
    """Send stage signal to Arduino."""
    global ser
    if ser is None or not ser.is_open:
        print("⚠️ Serial port not open. Attempting to reopen...")
        open_serial_port()

    if ser and stage in signals:
        try:
            ser.write(signals[stage].encode())
            print(f"✅ Sent Signal {signals[stage]} for {stage}")
        except serial.SerialException as e:
            print("❌ Failed to send signal:", e)
    else:
        print(f"⚠️ Invalid Stage or Serial Not Open: {stage}")

# ====== Routes ======
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

# ====== Upload and Processing ======
@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads."""
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

# File Serving
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

@app.route('/results/videos/<filename>')
def result_video(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename, mimetype='video/mp4')

# ====== Live Detection with Arduino Integration ======
camera = None

def generate_frames():
    """Live camera detection with YOLO and Arduino signal."""
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

        # Annotate detections and send signals
        for result in results[0].boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = result
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))  # Bounding box coordinates
            stage = model.names[int(cls)]  # Stage name

            # Send signal to Arduino
            send_stage_signal(stage)

            # Draw bounding box and label
            label = f"{stage} {conf:.2f}"
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
    return render_template('camera.html')

# ====== Additional Pages ======
@app.route("/performance")
def performance():
    return render_template("performance.html")

@app.route("/charts")
def charts():
    return render_template('charts.html')

@app.route("/logout")
def logout():
    return render_template("index.html")

# ====== Close Serial Port on App Exit ======
@app.before_request
def ensure_serial_open():
    if ser is None or not ser.is_open:
        open_serial_port()

@app.teardown_appcontext
def cleanup(exception=None):
    close_serial_port()

# ====== Run App ======
if __name__ == '__main__':
    try:
        app.run(debug=False)
    finally:
        close_serial_port()


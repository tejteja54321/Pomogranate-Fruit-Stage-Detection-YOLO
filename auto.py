from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response
import os
from ultralytics import YOLO
import cv2
from werkzeug.utils import secure_filename
import serial
import time
import threading

app = Flask(__name__)

# ====== Configurations ======
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.secret_key = 'supersecretkey'

# ====== Serial Communication ======
ser = None
last_sent_stage = None
last_sent_time = 0
SIGNAL_COOLDOWN = 1  # seconds

# ====== YOLO Model ======
model = YOLO(r'../runs/detect/train3/weights/best.pt')

# ====== Stage to Signal Mapping ======
signals = {
    'Bud': '1',
    'Flower': '2',
    'Early-Fruit': '3',
    'Mid-Growth': '4',
    'Ripe': '5'
}

# ====== Serial Port Functions ======
def open_serial_port():
    global ser
    try:
        ser = serial.Serial('COM4', 9600, timeout=1)
        print("✅ Serial port opened:", ser.portstr)
    except serial.SerialException as e:
        print("❌ Error opening serial port:", e)
        ser = None

def close_serial_port():
    global ser
    if ser and ser.is_open:
        ser.close()
        print("🔌 Serial port closed.")

def send_stage_signal(stage):
    global ser, last_sent_stage, last_sent_time
    current_time = time.time()

    if ser is None or not ser.is_open:
        open_serial_port()

    if stage in signals:
        if stage != last_sent_stage or (current_time - last_sent_time) > SIGNAL_COOLDOWN:
            try:
                ser.write(signals[stage].encode())
                print(f"✅ Sent Signal {signals[stage]} for {stage}")
                last_sent_stage = stage
                last_sent_time = current_time
            except serial.SerialException as e:
                print("❌ Failed to send signal:", e)
        else:
            print(f"⏳ Cooldown active. Skipping {stage}.")
    else:
        print(f"⚠️ Invalid Stage: {stage}")

# ====== Routes (UI Pages Optional) ======
@app.route('/')
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

@app.route("/performance")
def performance():
    return render_template("performance.html")

@app.route("/charts")
def charts():
    return render_template('charts.html')

@app.route("/logout")
def logout():
    return render_template("index.html")

# ====== Upload and Detect ======
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

        if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            result_video_path = process_video(file_path, filename)
            return render_template('image.html', original_file=filename, result_video=result_video_path)
        else:
            results = model(file_path)
            result_img_path = os.path.join(app.config['RESULTS_FOLDER'], f"result_{filename}")
            annotated_frame = results[0].plot()
            cv2.imwrite(result_img_path, annotated_frame)
            return render_template('image.html', original_file=filename, result_file=f"result_{filename}")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

@app.route('/results/videos/<filename>')
def result_video(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename, mimetype='video/mp4')

# ====== Video Processing Function ======
def process_video(path, filename):
    cap = cv2.VideoCapture(path)
    result_path = os.path.join(app.config['RESULTS_FOLDER'], f"result_{filename}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, verbose=False)
        for result in results[0].boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = result
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
            stage = model.names[int(cls)]
            send_stage_signal(stage)

            label = f"{stage} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if out is None:
            h, w = frame.shape[:2]
            out = cv2.VideoWriter(result_path, fourcc, 20.0, (w, h))
        out.write(frame)

    cap.release()
    out.release()
    return f"videos/result_{filename}"

# ====== Live Detection (Auto Run) ======
camera = None

def generate_frames():
    global camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Camera not opened.")
        return

    while True:
        success, frame = camera.read()
        if not success:
            break

        results = model.predict(frame, verbose=False)
        for result in results[0].boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = result
            x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
            stage = model.names[int(cls)]
            send_stage_signal(stage)

            label = f"{stage} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Live Detection", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

def auto_camera_start():
    for _ in generate_frames():
        pass

# ====== Startup Hooks ======
@app.before_request
def ensure_serial_open():
    if ser is None or not ser.is_open:
        open_serial_port()

@app.teardown_appcontext
def cleanup(exception=None):
    close_serial_port()

# ====== Run App with Auto Camera Detection ======
if __name__ == '__main__':
    try:
        open_serial_port()

        # 🔁 Start camera detection in background
        detection_thread = threading.Thread(target=generate_frames)
        detection_thread.daemon = True
        detection_thread.start()

        # 🚀 Start Flask App
        app.run(debug=False)

    finally:
        close_serial_port()

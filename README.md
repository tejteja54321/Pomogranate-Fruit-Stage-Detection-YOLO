# 🍎 Pomegranate Fruit Stage Detection using YOLOv10 🚀  

A complete AI + Web + IoT solution that classifies **pomegranate fruit stages** using **YOLOv10**, provides a **Flask-based web interface**, and triggers **hardware actions via Raspberry Pi**.

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![YOLOv10](https://img.shields.io/badge/YOLO-v10n-red)
![Flask](https://img.shields.io/badge/Flask-WebApp-lightgrey)
![RaspberryPi](https://img.shields.io/badge/Raspberry%20Pi-Hardware-green)

---

## 📚 Table of Contents

- [🔍 Overview](#-overview)
- [🛠️ Tech Stack](#-tech-stack)
- [🎯 YOLOv10 Model Training](#-yolov10-model-training)
- [🌐 Flask Web App Features](#-flask-web-app-features)
- [🔌 Hardware Integration](#-hardware-integration)
- [🔁 Serial Communication Mapping](#-serial-communication-mapping)
- [🚀 How to Run](#-how-to-run)
- [📁 Project Structure](#-project-structure)
- [🖼️ Demo](#-demo)
- [🙌 Credits](#-credits)
- [📝 License](#-license)

---

## 🔍 Overview

This project identifies **five growth stages** of a pomegranate fruit and sends corresponding signals to **Raspberry Pi hardware** using serial communication. It includes:

- **YOLOv10n-based model** trained on a custom dataset
- **Flask web application** for interaction
- **Raspberry Pi hardware integration** to automate physical actions (e.g., LED, pump, motor)

### 🍇 Detected Fruit Stages:

1. Bud  
2. Flower  
3. Early-Fruit  
4. Mid-Growth  
5. Ripe

---

## 🛠️ Tech Stack

| Layer         | Tools/Frameworks                        |
|---------------|-----------------------------------------|
| Model         | YOLOv10n (pretrained + custom trained)  |
| Backend       | Python, Flask                           |
| Frontend      | HTML, CSS, Bootstrap                    |
| Hardware      | Raspberry Pi, PySerial, GPIO            |
| Others        | OpenCV, NumPy                           |

---

## 🎯 YOLOv10 Model Training

- **Base Model**: `yolov10n.pt`
- **Dataset**: Custom-labeled pomegranate dataset (5 classes)
- **Training Output**:
  - `best.pt`: Best performing weights
  - `last.pt`: Final epoch weights
- **Inference Model**: `best.pt` is used in the Flask app for predictions

---

## 🌐 Flask Web App Features

| Page               | Description                                   |
|--------------------|-----------------------------------------------|
| **Home**           | Welcome page introducing the platform         |
| **Login/Register** | User authentication                          |
| **Upload Page**    | Upload image or video for detection           |
| **Live Detection** | Real-time camera detection using OpenCV       |
| **Performance Page** | Shows model accuracy, confidence, and metrics |
| **Charts**         | Displays graphical insights of detections     |

### 🔍 Additional Features:

- Real-time detection overlays using bounding boxes
- Detection results control hardware actions
- Clean Bootstrap-based UI

---

## 🔌 Hardware Integration

Raspberry Pi Pico is used to interface with external components such as DC motors, spraying mechanisms, and robotic arms for real-time action based on AI detection output from the YOLO model. The hardware performs physical tasks like spraying pesticides or plucking fruits depending on the pomegranate fruit stage detected.

- **Serial communication** is established using the `run.py` script
- A run.py script establishes serial communication between the AI-based detection system and the Raspberry Pi Pico microcontroller.

- Based on the detection output (Stage 1 to 5), numeric codes are sent to the Raspberry Pi Pico to perform specific actions.

- The robot receives these codes and triggers physical operations using motors and actuators.

### 🧠 Example Actions:

| Stage         | Hardware Action                          |
|---------------|------------------------------------------|
| Bud           | Activates the pesticide spraying system  |
| Early-Fruit   | Activates the pesticide spraying system  |
| Flower        | Activates the pesticide spraying system  |
| Mid-Growth    | Activates the plucking mechanism         |
| Ripe          | Activates the plucking mechanism         |


---

## 🔁 Serial Communication Mapping

| Stage         | Sent Code |
|---------------|-----------|
| Bud           | `1`       |
| Early-Fruit   | `2`       |
| Flower        | `3`       |
| Mid-Growth    | `4`       |
| Ripe          | `5`       |

Sent through serial port using PySerial in `run.py`.

---
### ⚙️ Hardware Components:

| Component                   | Description                                                                             |
|-----------------------------|-----------------------------------------------------------------------------------------|
| Raspberry Pi Pico           | Microcontroller used for receiving signals and controlling hardware actions.            |                                             
| DC Motor (100 RPM)          | Drives movement of the robot and mechanical arm.                                        |
| L293D Motor Driver Circuit  | Controls direction and speed of the DC motors.                                          |
| Pick and Place Mechanism    | Arm system designed to pluck the fruit or hold a sprayer for pesticide application.     |
| Sprayer Module	            | Electronically controlled pesticide spraying mechanism.                                 |
| Battery Pack	              | Powers the entire hardware system for portability.                                      |
| Chassis and Wheels		      | Physical base allowing mobility across fields.                                          |

---
## 🚀 How to Run

### 1️⃣ Clone the Repository
``` bash
git clone https://github.com/tejteja54321/Pomegranate-Fruit-Stage-Detection-YOLO.git
cd Pomegranate-Fruit-Stage-Detection-YOLO
```

### 2️⃣ Install Dependencies
``` bash
pip install -r requirements.txt
```

### 3️⃣ Run the Flask Web App (AI Detection System)
``` bash
python app.py
```

### 4️⃣ Run the Raspberry Pi Serial Communication Script (Hardware Control)
``` bash
Upload raspberry_code.ino file in hardware through aurdino software 
python main.py or python auto.py
```

### 5️⃣ Open in Browser
Visit http://127.0.0.1:5000 to access the web interface.

---
## 📁 Project Structure
``` php
Pomegranate-Fruit-Stage-Detection-YOLO/
│
├── yolov10/                    # YOLOv10n Model Files
│   ├── best.pt                 # Trained weights
│   └── yolov10n.pt             # Base model (optional)
│
├── templates/                  # HTML templates for Flask app
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── upload.html
│   └── live_detection.html
│   ├── performance.html
│   └── charts.html
│
├── static/                     # CSS, images, custom JS
│   └── css & js files
│
├── app.py                      # Flask backend
├── Aurdino_Code.ino            # Hardware Aurdino Code
├── Raspberrypi_ESP32_Code.ino  # Hardware Raspberry Pi ESP32 Code
├── run.py                      # Flask + Raspberry Pi GPIO + Serial controller
├── requirements.txt            # Required Python libraries
└── README.md                   # Project documentation

```
---

## 🖼️ Demo
**🧪 Screenshots and video demo will be added once the project is completed.
Stay tuned!**

---

## 🙌 Credits
- YOLOv10 model by WongKinYiu
- Flask framework by Pallets Projects
- Raspberry Pi hardware and GPIO libraries

---

## 📝 License
This project is **free to use** — just **ask for permission** before using it for personal, academic, or commercial purposes.


## 📬 Contact & Support
- 📧 Email: tejteja54321@gmail.com
- 🔗 GitHub: (https://github.com/tejteja54321/)
- 🌐 LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/teja-c-03a07320b/)

⭐ If you like this project, don't forget to give it a star! ⭐
👉 Star this repository 🚀

✅ 
**NOTE:** I Haven't uploaded dataset due to size limit if you need dataset please feel free to send mail or send message in LinkedIn

# 🍎 Pomegranate Fruit Stage Detection using YOLOv10 🚀  
A complete AI + Web + IoT solution to classify pomegranate fruit stages and trigger hardware responses using a Raspberry Pi.

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

This project detects and classifies **five different stages of pomegranate fruit** using the **YOLOv10n** model, integrates it into a **Flask web application**, and sends output to a **Raspberry Pi** via serial communication to control LEDs or any other connected hardware.

### 🌱 Detected Fruit Stages:
- **Bud**
- **Flower**
- **Early-Fruit**
- **Mid-Growth**
- **Ripe**

---

## 🛠️ Tech Stack

| Layer         | Tools/Frameworks               |
|---------------|-------------------------------|
| **Model**     | YOLOv10n (Pretrained, Fine-Tuned) |
| **Backend**   | Python, Flask                  |
| **Frontend**  | HTML, CSS, Bootstrap           |
| **Database**  | (Optional: SQLite/MySQL for login) |
| **Hardware**  | Raspberry Pi, Python Serial Communication |
| **Others**    | OpenCV, PySerial, NumPy        |

---

## 🎯 YOLOv10 Model Training

- **Base Model**: YOLOv10n (`yolov10n.pt`)
- **Training Dataset**: Custom dataset with 5 fruit stages
- **Output Models**:
  - `best.pt` – Best performing weights
  - `last.pt` – Last epoch weights
- **Model Format**: PyTorch `.pt`
- **Inference Script**: Used `best.pt` model for predictions in the Flask app

---

## 🌐 Flask Web App Features

| Page        | Description |
|-------------|-------------|
| **Home**    | Introduction to the platform |
| **Login/Register** | User authentication |
| **Upload Page** | Upload image/video for prediction |
| **Live Detection** | Real-time camera detection |

- Detection results are overlaid on images/videos using OpenCV.
- User-friendly UI built with Bootstrap.
- Automatic detection triggers further actions (e.g., hardware signal).

---

## 🔌 Hardware Integration

You connected a **Raspberry Pi** board to the Flask app using **serial communication**.

- Each detected fruit stage is mapped to a number.
- This data is sent to Raspberry Pi through a serial port.
- Based on received value, hardware performs actions (like turning ON specific LED or relays).

### Example Hardware Actions:
- **1**: Bud – Turn ON blue LED
- **2**: Early-Fruit – Turn ON yellow LED
- **3**: Flower – Turn ON pink LED
- **4**: Mid-Growth – Trigger pump for pesticides
- **5**: Ripe – Trigger motor for plucking

---

## 🔁 Serial Communication Mapping

| Stage         | Serial Code |
|---------------|-------------|
| Bud           | 1           |
| Early-Fruit   | 2           |
| Flower        | 3           |
| Mid-Growth    | 4           |
| Ripe          | 5           |

Serial connection is established using `pyserial` and the data is sent in the `run.py` file.

---


## 📁 Project Structure

pomegranate-fruit-stage-detection/
│
├── yolov10/                   # YOLOv10 model files
│   ├── best.pt
│   └── last.pt
│
├── templates/                 # HTML templates
│   ├── home.html
│   ├── login.html
│   ├── upload.html
│   └── live_detection.html
│
├── static/                    # CSS, JS, Images
│
├── app.py                     # Main Flask app
├── run.py                     # Serial communication script
├── requirements.txt
└── README.md


--- 


## 🚀 How to Run

### 1. Clone the Repo
```bash
git clone https://github.com/tejteja54321/Pomogranate-Fruit-Stage-Detection-YOLO.git
cd pomegranate-fruit-stage-detection

### 2. Setup Python Environment
```bash
pip install -r requirements.txt


### 3. Run the Flask App
```bash
python app.py

### 4. Run Serial Communication (Hardware Script)
```bash
python run.py

### 5. Access Web App
Go to http://127.0.0.1:5000 in your browser.


---




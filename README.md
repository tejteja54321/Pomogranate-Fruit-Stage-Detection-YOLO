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

| Page              | Description |
|-------------------|-------------|
| **Home**          | Welcome page |
| **Login/Register**| User authentication |
| **Upload Page**   | Upload image/video for detection |
| **Live Detection**| Real-time camera detection using OpenCV |

### 🔍 Additional Features:

- Real-time detection overlays using bounding boxes
- Detection results control hardware actions
- Clean Bootstrap-based UI

---

## 🔌 Hardware Integration

Raspberry Pi is used to interact with external components (like LEDs, motors) based on the detection result.

- **Serial communication** is established using the `run.py` script
- Hardware responses are triggered by values received from the AI detection output

### 🧠 Example Actions:

| Stage         | Hardware Action                 |
|---------------|----------------------------------|
| Bud           | Blue LED ON                     |
| Early-Fruit   | Yellow LED ON                   |
| Flower        | Pink LED ON                     |
| Mid-Growth    | Trigger pesticide sprayer       |
| Ripe          | Trigger fruit plucking mechanism|

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

## 🚀 How to Run

### 1️⃣ Clone the Repository
``` bash
git clone https://github.com/tejteja54321/Pomegranate-Fruit-Stage-Detection-YOLO.git
cd Pomegranate-Fruit-Stage-Detection-YOLO

---

``bash
### Run

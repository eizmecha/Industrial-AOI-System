# 🏭 Industrial Automated Optical Inspection (AOI) System

## 📌 Project Overview
This project demonstrates an end-to-end **Industrial Computer Vision System** designed for manufacturing pipelines. It utilizes **Azure Custom Vision (Transfer Learning & ResNet)** to automatically detect casting defects in submersible pump impellers, bridging the gap between Cloud AI and local PLC control systems.

## ⚙️ Core Technologies
* **AI Model:** Azure AI Vision (Custom Vision)
* **Architecture:** General (Compact) for edge-deployment readiness.
* **Logic Controller:** Python REST API integration.
* **Domain:** Mechatronics & Industry 4.0

## 🚀 How It Works
1. **Data Acquisition:** The system reads an image simulating an industrial camera feed.
2. **Cloud Inference:** Sends the binary image data to the trained Azure model via HTTP POST request.
3. **Control Signal Generation:** If a defect is detected with high confidence (>80%), a simulated `HIGH` signal is generated to trigger a pneumatic rejection arm on the conveyor belt.

## 📊 Model Performance
* **Precision:** 100.0%
* **Recall:** 100.0%
* **mAP:** 100.0%
*(Trained on 800 perfectly balanced industrial images).*
```markdown
# 🏭 Industrial Automated Optical Inspection (AOI) System

## 📌 Project Overview
This project demonstrates an end-to-end **Industrial Computer Vision System** designed for smart manufacturing pipelines. It utilizes **Azure Custom Vision (Transfer Learning & ResNet)** to automatically detect casting defects in submersible pump impellers, effectively bridging the gap between Cloud AI training and Local Edge deployment.

The system is now capable of **Offline Inference**, allowing it to run directly on the factory floor with zero latency and high security.

---

## 📂 Project Structure
```text
Industrial-AOI-System/
├── Defective_Parts/           # Dataset: Images of defective impeller castings
├── Perfect_Parts/             # Dataset: Images of normal impeller castings
├── Visuals/                   # Documentation and UI screenshots
│   ├── GUI_Defective_Sample.png
│   ├── GUI_Perfect_Sample.png
│   ├── Result_in_Custom_ai_vision.png
│   └── Result_in_VSCode.png
├── aoi_dashboard.py           # NEW: Modern Offline GUI (Edge AI)
├── inspection_system.py       # Legacy: Cloud-based inference script
├── model.onnx                 # Exported Edge AI model for local inference
├── labels.txt                 # Classification labels (OK, Defective)
├── test_image.jpeg            # Sample sensor image for validation
└── README.md                  # Project documentation
```

---

## ⚙️ Core Technologies
*   **AI Model:** Azure AI Vision (Custom Vision)
*   **Edge Engine:** ONNX Runtime (Offline Inference)
*   **GUI Framework:** CustomTkinter (Modern Industrial UI)
*   **Programming:** Python 3.x (OpenCV, NumPy, Pillow)
*   **Domain:** Mechatronics, Quality Assurance, & Industry 4.0

---

## 🚀 How It Works
The system supports two operational modes:

*   **Cloud Mode (`inspection_system.py`):** Uses the Azure REST API to send images to the cloud for analysis. Ideal for low-power devices with stable internet.
*   **Edge Mode (`aoi_dashboard.py`):** Uses the exported ONNX model for local, high-speed inference. This mode generates a **Control Signal (HIGH/LOW)** to trigger a pneumatic rejection arm if a defect is detected.

---

## 📊 Model Performance
*   **Precision:** 100.0%
*   **Recall:** 100.0%
*   **mAP:** 100.0%
*(Trained on 800 balanced industrial images).*

---

## 🖼️ User Interface
The system features a **Dark Mode Industrial Dashboard** that provides real-time feedback:

*   **Visual Feed:** Displays the current part under inspection.
*   **Status Indicator:** Green (OK) or Red (Defective).
*   **Confidence Score:** Real-time probability percentage.
*   **Conveyor Status:** Simulated PLC signal (Running/Halted).

---
*Developed by Ezaldeen A. Qassem as part of the Azure AI Engineering Diploma.*
```

This version includes the proper **text block** for your folder structure and **bullet points** for your technologies and UI features to ensure it renders perfectly on GitHub.

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import onnxruntime as ort
import numpy as np
import os

# ==========================================
# 1. System Initialization & Model Loading
# ==========================================
# Set the UI appearance to suit the industrial environment
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Load categories/labels (OK, Defective)
LABELS_PATH = "labels.txt"
MODEL_PATH = "model.onnx"

try:
    with open(LABELS_PATH, "r") as f:
        labels = [line.strip() for line in f.readlines()]
    # Start the local AI inference engine
    session = ort.InferenceSession(MODEL_PATH)
    input_name = session.get_inputs()[0].name
    print("[System] Offline AI Engine Loaded Successfully.")
except Exception as e:
    print(f"[Error] Failed to load AI engine: {e}")

# ==========================================
# 2. Main Dashboard Class
# ==========================================
class AOIDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Industrial AOI Control Panel - Offline Mode")
        self.geometry("900x600")
        
        # Grid layout (Two columns: one for the image, the other for controls)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # -- Left Frame: Image Display --
        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.image_label = ctk.CTkLabel(self.image_frame, text="No Image Loaded", font=("Arial", 20))
        self.image_label.pack(expand=True)

        # -- Right Frame: Controls & Results --
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.title_label = ctk.CTkLabel(self.control_frame, text="Vision System Status", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=30)

        self.upload_btn = ctk.CTkButton(self.control_frame, text="📸 Capture / Load Image", 
                                        font=("Arial", 16), height=50, command=self.load_image)
        self.upload_btn.pack(pady=20, padx=40, fill="x")

        self.result_label = ctk.CTkLabel(self.control_frame, text="Result: Waiting...", font=("Arial", 22))
        self.result_label.pack(pady=20)

        self.confidence_label = ctk.CTkLabel(self.control_frame, text="Confidence: --", font=("Arial", 18))
        self.confidence_label.pack(pady=10)
        
        self.plc_status = ctk.CTkLabel(self.control_frame, text="Conveyor: RUNNING 🟢", font=("Arial", 20, "bold"), text_color="green")
        self.plc_status.pack(pady=40)

    # ==========================================
    # 3. Image Processing & AI Inference
    # ==========================================
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            # Display the image on the interface
            img = Image.open(file_path)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(350, 350))
            self.image_label.configure(image=ctk_img, text="")
            
            # Send the image for analysis
            self.analyze_image(file_path)

    def analyze_image(self, img_path):
        try:
            # Preprocess the image to match Azure model dimensions (224x224)
            img = Image.open(img_path).convert("RGB")
            img = img.resize((224, 224))
            
            # Convert the image into mathematical arrays (Tensors)
            img_data = np.array(img).astype(np.float32)
            # Rearrange dimensions (Channels-First) and add the Batch dimension
            img_data = np.transpose(img_data, (2, 0, 1))
            img_data = np.expand_dims(img_data, axis=0)

            # Execute Inference
            outputs = session.run(None, {input_name: img_data})
            
            # ==========================================
            # 🎯 AZURE ONNX OUTPUT PARSING (THE ROBUST FIX)
            # outputs[1][0] is a dictionary: {'OK': 0.01, 'Defective': 0.99}
            # We find the max probability directly from the dictionary.
            # ==========================================
            prob_dict = outputs[1][0]
            
            # استخراج الفئة صاحبة أعلى نسبة مئوية مباشرة من القاموس
            predicted_label = max(prob_dict, key=prob_dict.get)
            confidence = float(prob_dict[predicted_label]) * 100

            self.update_ui(predicted_label, confidence)
            
        except Exception as e:
            self.result_label.configure(text=f"Error analyzing image", text_color="red")
            print(f"[Error] {e}")

    # ==========================================
    # 4. Update UI based on Logic
    # ==========================================
    def update_ui(self, label, confidence):
        self.confidence_label.configure(text=f"Confidence: {confidence:.2f}%")
        
        if label == "Defective":
            self.result_label.configure(text=f"Result: {label} ❌", text_color="red")
            self.plc_status.configure(text="Conveyor: HALTED 🚨\nRejection Arm Activated!", text_color="red")
        else:
            self.result_label.configure(text=f"Result: {label} ✅", text_color="green")
            self.plc_status.configure(text="Conveyor: RUNNING 🟢", text_color="green")

# Run the system
if __name__ == "__main__":
    app = AOIDashboard()
    app.mainloop()
import requests

# ==========================================
# 1. Cloud Connection Configuration
# ==========================================
# The Prediction URL for local image files (ending with /image)
PREDICTION_URL = "https://ezzlinkedincastingdata-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/f38b2140-91e5-463e-a2c9-db6566c75e67/classify/iterations/Iteration1/image"

# Paste your Prediction-Key (the pink text from Azure) here
PREDICTION_KEY ="YOUR_AZURE_SECRET_KEY_HERE"

# The path to the local image captured by the industrial camera
IMAGE_PATH = "test_image.jpeg"

# ==========================================
# 2. Data Packet Formulation
# ==========================================
# Setting the headers to authenticate and specify the data format (binary image)
headers = {
    'Prediction-Key': PREDICTION_KEY,
    'Content-Type': 'application/octet-stream'
}

print("\n[System] Booting up Automated Optical Inspection (AOI)...")
print("[System] Reading image from sensor...")

try:
    # Open the image in binary read mode ('rb')
    with open(IMAGE_PATH, 'rb') as image_data:
        print("[System] Sending image to Azure Custom Vision (Cloud Edge)...")
        
        # Send the HTTP POST request to the Azure Cloud
        response = requests.post(PREDICTION_URL, headers=headers, data=image_data)
        
        # Check if the connection was successful (HTTP 200 OK)
        if response.status_code == 200:
            results = response.json()
            
            # Extract the highest probability prediction
            top_prediction = results['predictions'][0]
            tag_name = top_prediction['tagName']
            probability = top_prediction['probability'] * 100
            
            print(f"\n✅ [Vision Output]: The part is classified as [{tag_name}] with {probability:.2f}% confidence.")
            
            # ==========================================
            # 3. PLC Integration & Control Logic
            # ==========================================
            print("-" * 50)
            if tag_name == "Defective" and probability > 80.0:
                print("🚨 [Control Signal]: High (1) -> ACTIVATE Pneumatic Rejection Arm!")
                print("🚨 [Status]: Defective part removed from conveyor belt.")
            else:
                print("🟢 [Control Signal]: Low (0) -> Conveyor Running Normal.")
                print("🟢 [Status]: Part passed quality inspection.")
            print("-" * 50)
            
        else:
            # Handle connection or authentication errors
            print(f"❌ [Error]: Cloud connection failed. Status code: {response.status_code}")
            print(response.text)

except FileNotFoundError:
    print(f"❌ [Error]: Camera failed to capture image. File '{IMAGE_PATH}' not found in the directory.")
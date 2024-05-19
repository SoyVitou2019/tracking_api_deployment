import requests
import numpy as np
import cv2
import json

# Load and preprocess your image
# image_path = 'D:/Github/tracking_api_deployment/testing_dataset/sct-mon1_2024-05-12_22-05-41.png'
image_path = './testing_dataset/study_img_1.png'
image = cv2.imread(image_path)
resized_image = cv2.resize(image, (224, 224))

# Convert image to list for JSON serialization
image_data = resized_image.tolist()

# Prepare the payload
data = {
    'feature': image_data
}

# Send the request to the FastAPI server
response = requests.post('http://127.0.0.1:8000/predict', json=data)

# Print the response from the server
print(response.json())

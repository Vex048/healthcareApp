import tensorflow as tf
import os
from pathlib import Path
import cv2
import numpy as np
class PneunomiaModelService:
    def __init__(self,model_path):
        self.model = None
        self.model_path = model_path
    
    def load_model(self):   
        self.model = tf.keras.models.load_model(self.model_path)
        
    def resize_img(self,img):
        # For Django uploaded files
        if hasattr(img, 'read'):
            img_bytes = img.read()  # Read the file-like object
            img_array = np.frombuffer(img_bytes, np.uint8)  # Use uint8, not float32
            img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)  # For grayscale (1 channel)

        # If it's already a numpy array, keep it as is
        if img is None:
            raise ValueError("Failed to decode the image")
            
        # Now resize
        image = cv2.resize(img, dsize=(224, 224))
        return image
    def preprocces_image(self,img):
        img = self.resize_img(img)
        image = tf.reshape(img,(1,224,224,1))
        return image
        
    def predict(self,image):
        prediction = self.model.predict(image)
        return prediction
    
    def interpret_result(self,pred):
        print(pred)
        num = pred[0][0]
        if int(num) == 1:
            return "The model detected pneunomia"
        else:
            return "The model didnt detect pneunomia"
        
        
MODEL_PATH = Path(PATH_TO_MODEL_PNEUNOMIA)
pneumonia_model = PneunomiaModelService(MODEL_PATH)
pneumonia_model.load_model()  

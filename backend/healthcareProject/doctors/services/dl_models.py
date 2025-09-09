import tensorflow as tf
import os
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import io
#from PIL import Image
class PneunomiaModelService:
    def __init__(self,model_path):
        self.model = None
        self.model_path = model_path
    
    def load_model(self):   
        self.model = tf.keras.models.load_model(self.model_path)
        
    def resize_img(self,img):
        if hasattr(img, 'read'):
            img_bytes = img.read()  
            img_array = np.frombuffer(img_bytes, np.uint8)  
            img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE) 

        if img is None:
            raise ValueError("Failed to decode the image")
            
        # Now resize
        image = cv2.resize(img, dsize=(224, 224))
        return image
    def preprocces_image(self,img):
        print(f"Image type: {type(img)}")
        
        
        img_data = img.read()
        img = Image.open(io.BytesIO(img_data))
        print(f"PIL Image: size={img.size}, mode={img.mode}")
        
        if img.mode != 'L':
            img = img.convert('L')
            print(f"Converted to grayscale: size={img.size}, mode={img.mode}")
            
        img = img.resize((224, 224))
        print(f"Resized: size={img.size}")
        
        img_array = np.array(img)
        print(f"Numpy array: shape={img_array.shape}, dtype={img_array.dtype}")
        
        
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1.255,  
            samplewise_center=True,
            samplewise_std_normalization=True
        )
        
        if len(img_array.shape) == 2:
            img_array = np.expand_dims(img_array, axis=-1)
        print(f"After adding channel dim: shape={img_array.shape}")
        img_array = np.expand_dims(img_array, 0)
        iterator = datagen.flow(img_array, batch_size=1)
        batch = next(iterator)
        print(f"After ImageDataGenerator: shape={batch.shape}, min={batch.min():.4f}, max={batch.max():.4f}")
        return batch
        
    def predict(self,image):
        prediction = self.model.predict(image)
        return prediction
    
    def interpret_result(self,pred):
        print(pred)
        prob = pred[0][0]
        if prob > 0.9:  
            return "The model detected pneumonia with high confidence"
        elif prob > 0.7:
            return "The model detected possible pneumonia (moderate confidence)"
        else:
            return "The model didn't detect pneumonia"
        
#MODEL_PATH = Path("C:/Projects/healthcare/healthcare/backend/healthcareProject/weights/pneunomia_model.h5")
MODEL_PATH = Path("D:/PythonProjects/TestDjangoVue/backend/healthcareProject/weights/pneunomia_model.h5")
pneumonia_model = PneunomiaModelService(MODEL_PATH)
pneumonia_model.load_model()  

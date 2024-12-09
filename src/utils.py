import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the keras Model
MODEL = load_model('saved_models/Chest_Disease_Classifier_Model.keras')
class_names = ['NORMAL', 'PNEUMONIA']

def predict(model, img):
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)

    # Use np.argmax to get the index of the highest probability
    predicted_class_index = np.argmax(predictions[0])
    predicted_class = class_names[predicted_class_index]
    confidence = round(100 * predictions[0][predicted_class_index], 2)
    return predicted_class, confidence
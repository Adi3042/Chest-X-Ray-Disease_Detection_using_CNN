import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import base64
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the Keras model
model = tf.keras.models.load_model('saved_models/Chest_Xray_Model.keras')

class_names = ['NORMAL', 'PNEUMONIA']

def predict(model, img):
    img = img.resize((128, 128))  # Resize image to match model input size
    img_array = np.expand_dims(np.array(img), axis=0).astype(np.float32) / 255.0

    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = round(100 * np.max(predictions[0]), 2)
    return predicted_class, confidence

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            img = Image.open(BytesIO(file.read()))
            predicted_class, confidence = predict(model, img)
            img_data = BytesIO()
            img.save(img_data, format='PNG')
            img_data.seek(0)
            img_base64 = base64.b64encode(img_data.getvalue()).decode('utf-8')
            return render_template(
                'index.html',
                img_data=img_base64,
                class_name=predicted_class,
                confidence=confidence
            )
    # Render fresh page on GET requests
    return render_template('index.html')

@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/aboutUs')
def about_us():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(debug=True)
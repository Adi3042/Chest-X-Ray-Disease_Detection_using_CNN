import numpy as np
from io import BytesIO
from PIL import Image
import base64
from flask import Flask, render_template, request
from src.utils import MODEL, class_names, predict
from src.logger import logging  # Import the logger
from waitress import serve

# Initialize the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Handles file upload and prediction.
    """
    if request.method == 'POST':
        file = request.files.get('file')  # Use .get() to avoid KeyError if 'file' is missing
        if file:
            try:
                img = Image.open(BytesIO(file.read()))
                logging.info("Image successfully opened.")
                
                predicted_class, confidence = predict(MODEL, img)
                logging.info(f"\nPrediction successful: {predicted_class} with confidence {confidence}%\n")
                
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
            except Exception as e:
                logging.error(f"Error during prediction: {e}")
                return render_template('index.html', error=str(e))
    # Render fresh page on GET requests
    logging.info("Rendering fresh page for GET request.")
    return render_template('index.html')

@app.route('/contactUs')
def contact_us():
    return render_template('/contactUs.html')

# Ensure the app instance is exposed for Gunicorn
if __name__ == '__main__':
    logging.info("Starting the Flask application.")
    serve(app, host='0.0.0.0', port=5000)

# Hosted at - http://127.0.0.1:5000/
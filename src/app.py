import sys
import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime

# --- Add FUnIE-GAN Project to Python's Path ---
# This allows us to import its code as a library.
# It assumes the FUnIE-GAN folder is located one level above this project's root.
funie_gan_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FUnIE-GAN', 'TF-Keras'))
if funie_gan_path not in sys.path:
    sys.path.append(funie_gan_path)

# --- Local Project Imports ---
# This imports the core image processing function from your src folder.
from src.core.enhancer import run_enhancement

# --- Constants & Configuration ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --- Initialize Flask App ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Create necessary folders if they don't exist.
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def enhance_image_route():
    """Handles the image upload and enhancement process."""
    # Check if a file was part of the request
    if 'image' not in request.files:
        return jsonify({"error": "No image file part in the request"}), 400
    
    file = request.files['image']
    
    # Check if a file was actually selected
    if file.filename == '':
        return jsonify({"error": "No image selected for upload"}), 400

    # Check if the file is valid and has an allowed extension
    if file and allowed_file(file.filename):
        # Create a secure, unique filename to prevent conflicts
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        
        # Save the original uploaded image to the server
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(saved_path)
        
        try:
            # Call the core enhancement logic from enhancer.py
            enhanced_path = run_enhancement(saved_path)
            
            # Return the path to the enhanced image for the frontend to display
            return jsonify({
                "message": "Enhancement successful",
                "enhanced_path": enhanced_path
            })
        except Exception as e:
            # Handle potential errors during the model processing
            print(f"Error during enhancement: {e}")
            return jsonify({"error": f"An error occurred during image processing: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Please upload a PNG, JPG, or JPEG."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)

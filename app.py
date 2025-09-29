import os
import sys
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# --- Add FUnIE-GAN to Python's path ---
# This allows us to import the enhancer script from the src directory
# and for the enhancer to find the FUnIE-GAN code.
funie_gan_path = os.path.abspath(os.path.join('..', 'FUnIE-GAN', 'TF-Keras'))
sys.path.append(funie_gan_path)

# --- Import the core enhancement logic ---
# This now correctly imports the function from enhancer.py
from src.core.enhancer import run_enhancement

# --- Initialize Flask App ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['OUTPUT_FOLDER'] = 'static/outputs/'

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


# --- API Endpoints ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')



@app.route('/enhance', methods=['POST'])
def enhance_image_route():
    """Handles the image upload and enhancement process."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        try:
            # The enhancer now returns the URL or raises an exception
            output_url = run_enhancement(input_path)
            if output_url is None:
                # Handle cases where enhancement fails without an exception
                raise ValueError("Enhancement function returned None")
            
            return jsonify({
                "original": f"/static/uploads/{filename}",
                "enhanced": output_url
            })
        except Exception as e:
            # IMPORTANT: Now we send a 500 Internal Server Error status
            print(f"Error during enhancement: {e}")
            return jsonify({"error": str(e)}), 500 # Return 500 status code

    return jsonify({"error": "An unknown error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)


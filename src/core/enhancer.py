import sys
import os
import cv2
import numpy as np

# --- Add FUnIE-GAN to Python's path ---
# This line finds the FUnIE-GAN folder, which is located one level above your app folder.
funie_gan_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'FUnIE-GAN', 'TF-Keras'))

# --- Check if the path exists ---
if not os.path.exists(funie_gan_path):
    raise ImportError("Could not find the FUnIE-GAN project. Please ensure it is side-by-side with your 'underwater-ai-enhancement' folder.")
sys.path.append(funie_gan_path)

# --- Import FUnIE-GAN modules ---
try:
    from nets import funieGAN
    from utils import data_utils
except ImportError as e:
    raise ImportError(f"Could not import FUnIE-GAN modules. Error: {e}")

# --- Global Model Loading ---
# Load the model only once when the application starts for efficiency.
print("Loading FUnIE-GAN model...")
try:
    # This creates an instance of the class, which builds the model.
    funie_gan_instance = funieGAN.FUNIE_GAN()
    generator = funie_gan_instance.generator
    
    # --- CRITICAL FIX: Load the pre-trained weights ---
    # Define the path to the pre-trained weights file
    weights_path = os.path.join(funie_gan_path, 'models', 'gen_p', 'model_15320_.h5')
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Could not find the model weights file at: {weights_path}")
    
    # Load the weights into the generator model
    generator.load_weights(weights_path)
    print("FUnIE-GAN model and weights loaded successfully.")

except Exception as e:
    print(f"FATAL: Failed to load FUnIE-GAN model. Error: {e}")
    generator = None

def run_enhancement(input_path):
    """
    Enhances an underwater image using the pre-loaded FUnIE-GAN model.
    """
    if generator is None:
        raise RuntimeError("FUnIE-GAN model is not loaded. Cannot process image.")

    # Use the correct 'read_and_resize' function from the FUnIE-GAN utils.
    # The model expects 256x256 images.
    im = data_utils.read_and_resize(input_path, img_res=(256, 256))

    # Preprocess the image to the [-1, 1] range the model expects
    im = data_utils.preprocess(im)

    # Check for 4-channel images (like PNGs with transparency) and convert to 3-channel
    if im.shape[2] == 4:
        im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
    
    # Run the enhancement
    gen_img = generator.predict(np.expand_dims(im, 0))
    
    # Create a unique filename for the output
    base_name = os.path.basename(input_path)
    file_name, file_ext = os.path.splitext(base_name)
    output_filename = f"{file_name}_enhanced_{cv2.getTickCount()}{file_ext}"
    
    # Define the save path inside the static folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_path_disk = os.path.join(output_dir, output_filename)
    
    # Save the image using a corrected method
    # Deprocess the image from [-1, 1] to [0, 255]
    enhanced_image_to_save = data_utils.deprocess(np.squeeze(gen_img, 0))
    # Convert from RGB (PIL) to BGR (OpenCV) for saving
    enhanced_image_to_save_bgr = cv2.cvtColor(enhanced_image_to_save, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path_disk, enhanced_image_to_save_bgr)

    # Return a web-accessible URL for the frontend
    output_url = f"/static/outputs/{output_filename}"
    return output_url


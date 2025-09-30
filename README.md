## AI Underwater Image Enhancement for Maritime Security

This project is a web-based application designed to enhance the quality of underwater images using a deep learning model. It addresses critical challenges in maritime security operations, where underwater images suffer from poor visibility, color distortion, and low contrast due to light scattering and absorption in water.

By leveraging the FUnIE-GAN model, this tool provides clear, real-time enhancement of underwater visuals—useful for improving threat detection, navigation, and reconnaissance for Autonomous Underwater Vehicles (AUVs) and Remotely Operated Vehicles (ROVs).

### Features

- **Direct Image Upload**: Upload `.jpg`, `.jpeg`, `.png` images.
- **AI-Powered Enhancement**: Pre-trained FUnIE-GAN corrects color, reduces haze, and improves contrast.
- **Side-by-Side Comparison**: Instantly view original vs enhanced images.
- **Real-time Processing Log**: Status updates during processing.

### Technology Stack

- **Backend**: Python, Flask, TensorFlow
- **Frontend**: HTML, CSS, JavaScript
- **Core AI Model**: FUnIE-GAN (Fast Underwater Image Enhancement GAN)

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1) Prerequisites

- **Python 3.10** (recommended). Newer versions may cause dependency conflicts.
- **Git** for cloning repositories.

### 2) Clone the Repositories

Place both repositories side-by-side in the same parent folder.

```bash
# Navigate to the directory where you want to store your projects
cd path/to/your/projects

# Clone this application repository
git clone <your-app-repo-url> underwater-ai-enhancement

# Clone the FUnIE-GAN repository
git clone https://github.com/xahidbuffon/FUnIE-GAN.git
```

Expected structure:

```text
/projects/
├─ /FUnIE-GAN/
└─ /underwater-ai-enhancement/
```

### 3) Set Up the Python Environment

Create and activate a virtual environment inside the app folder.

```bash
# Navigate into your project folder
cd underwater-ai-enhancement

# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows (PowerShell/CMD)
.\venv\Scripts\activate
# On Git Bash (Windows)
source venv/Scripts/activate
```

When active, your prompt should start with `(venv)`.

### 4) Install Dependencies

```bash
# Ensure your (venv) is active
python -m pip install -r requirements.txt
```

## How to Run the Project

Activate your environment (if not already active) and start the server.

```bash
# Activate (if needed)
.\venv\Scripts\activate   # Windows PowerShell/CMD
# or
source venv/Scripts/activate # Git Bash on Windows

# Start the Flask server
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

You should now see the AI Underwater Image Enhancement dashboard, ready to process your images.

document.addEventListener('DOMContentLoaded', () => {
    // --- Element Sanity Check ---
    // This block checks if all required HTML elements exist before running any code.
    const requiredElementIds = [
        'file-input', 'file-name', 'enhance-btn',
        'original-image-box', 'enhanced-image-box', 'log', 'spinner'
    ];
    for (const id of requiredElementIds) {
        if (!document.getElementById(id)) {
            console.error(`Critical Error: HTML element with id "${id}" was not found. The application cannot start.`);
            return; // Stop the script if a required element is missing.
        }
    }

    // Get references to all the necessary HTML elements using the correct IDs from your HTML
    const fileInput = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');
    const enhanceBtn = document.getElementById('enhance-btn');
    const originalImageBox = document.getElementById('original-image-box');
    const enhancedImageBox = document.getElementById('enhanced-image-box');
    const logOutput = document.getElementById('log');
    const loadingSpinner = document.getElementById('spinner');

    let selectedFile = null;

    // --- Event Listener for File Selection ---
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            selectedFile = file;
            fileNameDisplay.textContent = file.name;
            updateLog('Image selected. Click "Enhance Image" to process.');
            enhanceBtn.disabled = false; // Enable the enhance button

            // Use FileReader to show a preview of the selected image
            const reader = new FileReader();
            reader.onload = (e) => {
                // Create an img element for the preview and add it to the box
                originalImageBox.innerHTML = ''; // Clear the "Waiting..." text
                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = "Original underwater image";
                originalImageBox.appendChild(img);
            };
            reader.readAsDataURL(file);
        } else {
            enhanceBtn.disabled = true; // Disable if no file is selected
        }
    });

    // --- Function to Handle the Enhancement Process ---
    async function handleEnhance() {
        if (!selectedFile) {
            updateLog('Please select an image first.');
            return;
        }

        updateLog('Enhancing image... This may take a moment.');
        loadingSpinner.style.display = 'block';
        enhancedImageBox.innerHTML = '<div class="spinner" id="spinner" style="display: block;"></div><p>Result will appear here.</p>'; // Reset enhanced box

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch('/enhance', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Server responded with status: ${response.status}`);
            }

            const data = await response.json();
            
            // Create an img element for the result and add it to the box
            enhancedImageBox.innerHTML = ''; // Clear the spinner and text
            const img = document.createElement('img');
            img.src = data.enhanced;
            img.alt = "Enhanced underwater image";
            enhancedImageBox.appendChild(img);

            updateLog('Enhancement successful!');

        } catch (error) {
            console.error('Enhancement Error:', error);
            updateLog(`Error: ${error.message}`);
        } finally {
            // The spinner is inside the enhancedImageBox, so it's removed automatically.
            // We can ensure it's hidden if the element still exists for any reason.
            const finalSpinner = document.getElementById('spinner');
            if(finalSpinner) finalSpinner.style.display = 'none';
        }
    }

    // --- Helper Function to Update the Log Display ---
    function updateLog(message) {
        if (logOutput) {
            logOutput.textContent = message;
        } else {
            console.log(`Log: ${message}`);
        }
    }

    // --- Attach the handleEnhance function to the button's click event ---
    enhanceBtn.addEventListener('click', handleEnhance);
});


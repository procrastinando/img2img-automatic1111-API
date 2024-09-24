# Img2Img Inpainting Web Application
### Overview
This application provides a web-based interface for performing image-to-image (img2img) inpainting using Stable Diffusion. It allows users to upload an initial image and a mask, input various parameters, and generate a new image based on these inputs.
### Technologies Used

- Python: The core programming language used for the application.
- Streamlit: A Python library for creating web applications with minimal front-end experience.
- Requests: A Python HTTP library used for making API calls to the Stable Diffusion WebUI.
- Pillow (PIL): Python Imaging Library, used for image processing tasks.
- Base64: A module used for encoding and decoding the image data.
- Stable Diffusion WebUI: The backend API that performs the actual img2img inpainting process.

### Key Features

- Web-based user interface for img2img inpainting
- Image upload functionality for both initial image and mask
- Customizable parameters including:
```
Prompt
Steps
CFG Scale
Image dimensions (width and height)
Denoising strength
Mask blur
Inpainting mask inversion
```

- Integration with Stable Diffusion WebUI API
- Real-time image generation and display

### Workflow

- User inputs the Stable Diffusion WebUI API URL
- User uploads an initial image and a mask image
- User adjusts various parameters for the inpainting process
- Application sends a POST request to the Stable Diffusion WebUI API
- Received image data is decoded and displayed in the web interface

### Technical Notes

- The application uses base64 encoding for image data transmission.
- It leverages Streamlit's reactive programming model for real-time updates.
- The Stable Diffusion WebUI must be running with the --api flag enabled for this application to function.
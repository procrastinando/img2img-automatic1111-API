import streamlit as st
import requests
import base64
from PIL import Image
import io

st.set_page_config(page_title="img2img API", page_icon="icon.webp")
st.title("Img2Img Inpainting Web App")

def load_image_as_base64(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def run_img2img(url, init_image, mask_image, prompt, steps, cfg_scale, width, height, denoising_strength, mask_blur, inpainting_mask_invert):
    payload = {
        "init_images": [load_image_as_base64(init_image)],
        "mask": load_image_as_base64(mask_image),
        "prompt": prompt,
        "negative_prompt": "",
        "styles": [],
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "batch_size": 1,
        "n_iter": 1,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height,
        "restore_faces": False,
        "tiling": False,
        "denoising_strength": denoising_strength,
        "mask_blur": mask_blur,
        "inpainting_fill": 2,
        "inpaint_full_res": True,
        "inpainting_mask_invert": inpainting_mask_invert,
        "override_settings": {
            "sd_model_checkpoint": "v1-5-pruned-emaonly.safetensors"
        },
        "script_name": "",
        "send_images": True,
        "save_images": False
    }

    response = requests.post(url=f"{url}/sdapi/v1/img2img", json=payload)
    r = response.json()
    
    output_image_base64 = r['images'][0]
    output_image_data = base64.b64decode(output_image_base64)
    return Image.open(io.BytesIO(output_image_data))


api_url = st.text_input("Enter the WebUI API URL:", "http://127.0.0.1:7860")
prompt = st.text_input("Enter your prompt:", "small leaves")

col1, col2 = st.columns(2)

with col1:
    steps = st.slider("Steps", min_value=1, max_value=150, value=20)
    cfg_scale = st.slider("CFG Scale", min_value=1.0, max_value=30.0, value=7.0, step=0.5)
    width = st.number_input("Width", min_value=64, max_value=2048, value=512, step=64)
    height = st.number_input("Height", min_value=64, max_value=2048, value=512, step=64)

with col2:
    denoising_strength = st.slider("Denoising Strength", min_value=0.0, max_value=1.0, value=0.75, step=0.05)
    mask_blur = st.slider("Mask Blur", min_value=0, max_value=64, value=4)
    inpainting_mask_invert = st.checkbox("Invert Mask")

init_image = st.file_uploader("Upload the initial image", type=["png", "jpg", "jpeg"])
mask_image = st.file_uploader("Upload the mask image", type=["png", "jpg", "jpeg"])

if st.button("Run Img2Img Inpainting"):
    if init_image is not None and mask_image is not None:
        with st.spinner("Processing..."):
            result_image = run_img2img(
                api_url, init_image, mask_image, prompt, 
                steps, cfg_scale, width, height, 
                denoising_strength, mask_blur, int(inpainting_mask_invert)
            )
        st.image(result_image, caption="Result", use_column_width=True)
    else:
        st.error("Please upload both an initial image and a mask image.")

st.sidebar.markdown("""
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
""")
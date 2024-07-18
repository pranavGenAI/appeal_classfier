import streamlit as st
from transformers import AutoModel, AutoProcessor
from PIL import Image
import torch

# Load the model and processor
model_name = "OpenGVLab/InternVL2-Llama3-76B"
model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
processor = AutoProcessor.from_pretrained(model_name)

# Streamlit app
st.title("Image to Text Converter")
st.write("Upload an image to convert it to text.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    with st.spinner('Processing...'):
        # Preprocess the image
        inputs = processor(images=image, return_tensors="pt")
        
        # Generate text
        with torch.no_grad():
            outputs = model(**inputs)
            # Assuming the model outputs can be decoded to text
            # This is model-specific and should be adapted accordingly
            generated_text = outputs["text"]

        st.success('Done!')
        st.write("Generated Text:")
        st.write(generated_text)

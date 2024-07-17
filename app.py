import streamlit as st
import numpy as np
from paddleocr import PaddleOCR
import cv2

# Initialize PaddleOCR
ocr = PaddleOCR()

def ocr_image(image):
    # Perform OCR on the image
    result = ocr.ocr(image)
    extracted_text = ''
    for line in result:
        for word_info in line:
            extracted_text += word_info[1] + ' '
        extracted_text += '\n'
    return extracted_text

def main():
    st.title("Image to Text Conversion with PaddleOCR")
    st.write("Upload an image and get text from it.")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Read the image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Display the image
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Perform OCR
        text = ocr_image(image)

        # Display extracted text
        st.header("Extracted Text:")
        st.write(text)

if __name__ == '__main__':
    main()

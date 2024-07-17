import streamlit as st
import PIL.Image
import google.generativeai as genai

st.set_page_config(page_title="Appeal Classifier", page_icon = ">")

# Configure Google Generative AI with the API key
GOOGLE_API_KEY = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
genai.configure(api_key=GOOGLE_API_KEY)
st.image("https://www.vgen.it/wp-content/uploads/2021/04/logo-accenture-ludo.png", width=150)
st.markdown("""
    <style>
    .stButton button {
        background: linear-gradient(120deg,#FF007F, #A020F0 100%) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to interact with the Generative AI model
def generate_content(image):
    try:
        # Initialize the GenerativeModel
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = """You have been given appeal summary as input. Now you will help me in classifying the the provided appeal summary using the logic provided to you.
        Classification Logic:
        Category PA ASO: If funding value is either ASO, NON ERISA ASO, ADMIN, MED NEC. Part/Provider: Provider 
        Category MA ASO: If funding value is either ASO, NON ERISA ASO, ADMIN, MED NEC. Part/Provider: Participant
        Category PA NON ASO NON PRIORITY STATES: If funding value is either TRAD, CMP, RCM. Part/Provider: Provider
        Category MA OTHER NON ASO PRIORITY STATES: If funding value is either TRAD, CMP, RCM . Part/Provider: Participant
        Category PA TX NON ASO: If funding value is either TRAD, CMP, RCM. Part/Provider: Provider. State Processed: TX

        Check the above condition and then write the classification category with the rationale.        

        """
        # Generate content using the image
        response = model.generate_content([prompt, image], stream=True)
        response.resolve()
        return response.text  # Return generated text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

def main():
    st.title("Appeal Classifier")

    # File uploader for multiple images
    uploaded_images = st.file_uploader("Upload appeal summary images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_images:
        for uploaded_image in uploaded_images:
            # Display uploaded image
            st.image(uploaded_image, caption="Uploaded Appeal Summary", use_column_width=True)

            # Convert uploaded image to PIL image object
            image = PIL.Image.open(uploaded_image)

            # Determine button label based on number of uploaded images
            if len(uploaded_images) > 1:
                button_label = f"Classify Appeal {uploaded_images.index(uploaded_image) + 1}"
            else:
                button_label = "Classify Appeal"

            # Button to classify appeal
            if st.button(button_label):
                with st.spinner("Evaluating..."):
                    # Generate content using the image
                    generated_text = generate_content(image)

                    # Display generated content
                    if generated_text:
                        st.subheader("Classification:")
                        st.write(generated_text)
                        st.markdown("***")

if __name__ == "__main__":
    main()

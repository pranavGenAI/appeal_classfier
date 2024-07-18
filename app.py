import streamlit as st
import PIL.Image
import google.generativeai as genai
import time
import hashlib
import json

# Set page title, icon, and dark theme
st.set_page_config(page_title="Appeals Classifier: Categorize appeal document", page_icon=">")
st.markdown(
    """
    <style>
    .stButton button {
        background: linear-gradient(120deg,#FF007F, #A020F0 100%) !important;
        color: white !important;
    }
    body {
        color: white;
        background-color: #1E1E1E;
    }
    .stTextInput, .stSelectbox, .stTextArea, .stFileUploader {
        color: white;
        background-color: #2E2E2E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Configure Google Generative AI with the API key
GOOGLE_API_KEY = "AIzaSyCNX1H0w4y7dJPlwqvrxiW1OjAMf4dkFp0"
genai.configure(api_key=GOOGLE_API_KEY)
st.image("https://www.vgen.it/wp-content/uploads/2021/04/logo-accenture-ludo.png", width=150)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Define users and hashed passwords for simplicity
users = {
    "ankur.d.shrivastav": hash_password("ankur123"),
    "sashank.vaibhav.allu": hash_password("sashank123"),
    "shivananda.mallya": hash_password("shiv123"),
    "pranav.baviskar": hash_password("pranav123")
}

def login():
    col1, col2= st.columns([0.6, 0.4])  # Create three columns with equal width
    with col1:  # Center the input fields in the middle column
        st.title("Login")
        st.write("Username")
        username = st.text_input("")
        st.write("Password")
        password = st.text_input("", type="password")
        
        if st.button("Sign in"):
            hashed_password = hash_password(password)
            if username in users and users[username] == hashed_password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.experimental_rerun()  # Refresh to show logged-in state
            else:
                st.error("Invalid username or password")

def logout():
    # Clear session state on logout
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.experimental_rerun()  # Refresh to show logged-out state

# Function to interact with the Generative AI model
def generate_content(image):
    try:
        # Initialize the GenerativeModel
        model = genai.GenerativeModel('gemini-1.5-pro')
        prompt = """You have been given appeal summary as input. Now you will help me in classifying the the provided appeal summary using the logic provided to you.
        Classification Logic:
        Category PA ASO: If funding value is either ASO, NON ERISA ASO, ADMIN, MED NEC. Part/Provider: Provider 
        Category MA ASO: If funding value is either ASO, NON ERISA ASO, ADMIN, MED NEC. Part/Provider: Participant
        Category PA NON ASO PRIORITY STATES: If funding value is either TRAD, CMP, RCM. Part/Provider: Provider
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
    st.title("Appeals Classifier")

    # File uploader for multiple images
    uploaded_images = st.file_uploader("Upload appeal summary images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_images:
        for uploaded_image in uploaded_images:
            # Display uploaded image
            st.image(uploaded_image, caption="", use_column_width=True)

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
    if st.session_state.logged_in:
        st.sidebar.write(f"Welcome, {st.session_state.username}")
        if st.sidebar.button("Logout"):
            logout()
        main()
    else:
        login()

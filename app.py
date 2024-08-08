import streamlit as st
import PIL.Image
import google.generativeai as genai
import time
import hashlib
import json
# Set page title, icon, and dark theme
st.set_page_config(page_title="Appeals Classifier: Categorize appeal document", page_icon=">", layout="wide")
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
#GOOGLE_API_KEY = st.secrets['GEMINI_API_KEY']
GOOGLE_API_KEY = "AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw"
genai.configure(api_key=GOOGLE_API_KEY)

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
    col1, col2= st.columns([0.3, 0.7])  # Create three columns with equal width
    with col1:  # Center the input fields in the middle column
        st.title("Login")
        st.write("Username")
        username = st.text_input("",  label_visibility="collapsed")
        st.write("Password")
        password = st.text_input("", type="password",  label_visibility="collapsed")
        
        if st.button("Sign in"):
            hashed_password = hash_password(password)
            if username in users and users[username] == hashed_password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                st.rerun()  # Refresh to show logged-in state
            else:
                st.error("Invalid username or password")

def logout():
    # Clear session state on logout
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully!")
    st.rerun()  # Refresh to show logged-out state

# Path to the logo image
logo_url = "https://www.vgen.it/wp-content/uploads/2021/04/logo-accenture-ludo.png"

def generate_content(image):
    max_retries = 10
    delay = 10
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Initialize the GenerativeModel
            print("Model definition")
            model = genai.GenerativeModel('gemini-1.5-pro')
            prompt = """You have been given appeal summary as input. Now you will help me in classifying the provided appeal summary using the logic provided to you.
            Classification Logic:
            Category PA ASO: If funding value is either ASO, NON ERISA ASO, ADMIN, MED NEC. Part/Provider: Provider 
            Category MA ASO: If funding value is either ASO, NON ERISA ASO, ADMIN, MED NEC. Part/Provider: Participant
            Category PA NON ASO PRIORITY STATES: If funding value is either TRAD, CMP, RCM. Part/Provider: Provider
            Category MA OTHER NON ASO PRIORITY STATES: If funding value is either TRAD, CMP, RCM. Part/Provider: Participant
            Category PA TX NON ASO: If funding value is either TRAD, CMP, RCM. Part/Provider: Provider. State Processed: TX
    
            Check the above condition and then write the classification category with the rationale.        
            """
            # Generate content using the image
            print("Model generate")
            response = model.generate_content([prompt, image], stream=True)
            response.resolve()
            print("Response text", response.text)
            return response.text  # Return generated text
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                st.error(f"Error generating content: Server not available. Please try again after sometime")
            time.sleep(delay)
    
    # Return None if all retries fail
    return None

def main():
    st.title("Appeals Classifier")
    col1, col2, col3 = st.columns([4,1,4])
    generated_text = ""
    with col1:
        # File uploader for multiple images
        uploaded_images = st.file_uploader("Upload appeal summary images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)   
        if uploaded_images:
            for uploaded_image in uploaded_images:
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

                st.image(uploaded_image, caption="", use_column_width=True)
    
    with col3:
        if generated_text:
            st.markdown(
                f"""
                <div class="generated-text-box">
                    <h3>Classification Result:</h3>
                    <p>{generated_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("***")

if __name__ == "__main__":
    if st.session_state.logged_in:
        col1,col2,col3 = st.columns([10,10,1.5])
        with col3:
            if st.button("Logout"):
                logout()
        main()
    else:
        login()


# Custom CSS for the header and logo
# Custom CSS for the header and logo
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Graphik:wght@400;700&display=swap');

    body {
        background-color: #f0f0f0;
        color: black;
        font-family: 'Graphik', sans-serif;
    }
    .main {
        background-color: #f0f0f0;
    }
    .stApp {
        background-color: #f0f0f0;
    }
    header {
        background-color: #660094 !important;
        padding: 10px 40px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .logo {
        height: 30px;
        width: auto;
        margin-right: 20px;  /* Space between logo and next item */
    }
    .header-content {
        display: flex;
        align-items: center;
    }
    .header-right {
        display: flex;
        align-items: center;
    }

    h1 {
        color: black;
        margin: 0;
        padding: 0;
    }

    .generated-text-box {
        border: 3px solid transparent; /* Set border to transparent to use background for the border */
        padding: 20px;
        border-radius: 10px; /* Rounded corners */
        color: black; /* Text color */
        background-image: linear-gradient(120deg, #FF007F, #A020F0); /* Gradient background */
        background-clip: padding-box; /* Ensure the gradient does not cover the border area */
        border-image: linear-gradient(120deg, #FF007F, #A020F0) 1; /* Gradient border */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Adding the logo and other elements in the header
st.markdown(
    f"""
    <header tabindex="-1" data-testid="stHeader" class="st-emotion-cache-12fmjuu ezrtsby2">
        <div data-testid="stDecoration" id="stDecoration" class="st-emotion-cache-1dp5vir ezrtsby1"></div>
        <div class="header-content">
            <!-- Add the logo here -->
            <img src="https://www.vgen.it/wp-content/uploads/2021/04/logo-accenture-ludo.png" class="logo" alt="Logo">
        
    </header>

    """,
    unsafe_allow_html=True
)


import streamlit as st
import base64
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
#from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import LLMChain
from langchain.schema import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import HumanMessagePromptTemplate
from streamlit_extras.stylable_container import stylable_container
import pytesseract
import fitz 
from PIL import Image
import io
from tika import parser


st.set_page_config(page_title="Appeal Classifier", layout="wide")

st.image("https://www.vgen.it/wp-content/uploads/2021/04/logo-accenture-ludo.png", width=150)
st.markdown("""
    <style>
    .stButton button {
        background: linear-gradient(120deg,#FF007F, #A020F0 100%) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
   
    <h1>
        Appeal Classifier
    </h1>
""", unsafe_allow_html=True)

api_key = 'AIzaSyCiPGxwD04JwxifewrYiqzufyd25VjKBkw'


def get_conversational_chain():
    prompt_template = """
    
    Context:\n {context}?\n
    Question: \n{question}\n . 

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=api_key)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    print("Prompt ***** --->", prompt)
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question, api_key):
    # Embeddings and vector store initialization omitted for brevity
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    # Perform similarity search and get response
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("Response: ", response["output_text"])


def main():
    st.markdown("")
    pdf_docs = st.file_uploader("Upload appeal document in PDF format and Click on the Submit & Process Button", accept_multiple_files=True, key="pdf_uploader")
    
    with st.spinner("Processing..."):
        if st.button("Submit & Process", key="process_button", help="Click to submit and process"):
            text = "Appeal: "
            
            for pdf_data in pdf_docs:
                pdf_bytes = pdf_data.read()
                pdf_document = fitz.open(stream=pdf_bytes, filetype="bytes")
                
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    images = page.get_images(full=True)
                    
                    for img_index, img in enumerate(images):
                        xref = img[0]
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"] 
                        image = Image.open(io.BytesIO(image_bytes))
                        parsed = parser.from_buffer(image_bytes)
                        text += parsed['content']
                
                pdf_document.close()
                text += "\n\nResponse 2: "
            
            st.write(text)
            st.success("Done")

def extract_images_from_pdf(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(image_bytes)
    return images


if __name__ == "__main__":
    main()

import os
import requests
import streamlit as st
import pymupdf  # Correct import for PyMuPDF
import docx2txt  # Better alternative to python-docx
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter  # ✅ NEW: For chunking

# 🔑 Securely Load OpenAI API Key
os.environ["OPENAI_API_KEY"] = "<api key>"


# Streamlit UI Setup
st.set_page_config(page_title="🔍 Chat with Website & Documents", layout="wide")
st.title("🤖 Chat with Websites & Documents (With Chunking)")

st.sidebar.header("🔗 Enter Website URL to Scrape")
url = st.sidebar.text_input("Website URL", "https://example.com")

# Initialize session state for content storage
if "content" not in st.session_state:
    st.session_state.content = ""

# Function to fetch and parse website content
def fetch_website_content(url):
    """Fetches and extracts readable text from a website."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract meaningful content from <p> and <li> tags
        text = "\n".join([p.get_text(strip=True) for p in soup.find_all(["p", "li"]) if p.get_text(strip=True)])

        return text if text else None

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching website: {e}")
        return None

# Function to chunk text
def chunk_text(text, chunk_size=50000, chunk_overlap=5000):
    """Splits long text into smaller chunks with overlap for better AI context."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

# Scrape Website and Store Content
if st.sidebar.button("Scrape Website"):
    with st.spinner("Scraping and processing website content..."):
        website_text = fetch_website_content(url)

        if website_text:
            chunks = chunk_text(website_text)  # ✅ NEW: Chunking applied
            st.session_state.content = "\n\n".join(chunks[:5])  # ✅ Store first 5 chunks
            st.success("✅ Website content scraped and chunked! Start chatting below.")
        else:
            st.error("⚠️ No readable content extracted from the website.")

# File Upload for PDF, DOCX, TXT
st.sidebar.header("📂 Upload a Document")
uploaded_file = st.sidebar.file_uploader("Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("Processing file..."):
        file_text = ""

        if uploaded_file.type == "application/pdf":
            pdf_doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
            file_text = "\n".join([page.get_text("text") for page in pdf_doc])

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            file_text = docx2txt.process(uploaded_file)

        elif uploaded_file.type == "text/plain":
            file_text = uploaded_file.read().decode("utf-8")

        chunks = chunk_text(file_text)  # ✅ NEW: Chunking applied
        st.session_state.content = "\n\n".join(chunks[:5])  # ✅ Store first 5 chunks
        st.success("✅ File content loaded and chunked! Start chatting below.")

# Chat with Content
st.subheader("💬 Chat with the Website or Document")

query = st.text_input("Ask a question")

if st.button("Ask AI"):
    if query:
        if not st.session_state.content:
            st.warning("⚠️ No content available! Please scrape a website or upload a file first.")
        else:
            with st.spinner("Generating response..."):
                try:
                    # Initialize OpenAI GPT model
                    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

                    # Construct structured prompt
                    prompt = f"""
                    You are an AI assistant. Below is content extracted from a website or document.

                    === Content Source ===
                    {st.session_state.content}

                    === Question ===
                    {query}

                    Provide a clear and concise answer.
                    """

                    # Get response from GPT
                    response = llm.invoke(prompt)

                    # Display AI response
                    st.subheader("🤖 AI Response:")
                    st.write(response)

                except Exception as e:
                    st.error(f"❌ Error during chat: {e}")

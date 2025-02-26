import streamlit as st
import os
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 🔑 Securely Load OpenAI API Key
os.environ["OPENAI_API_KEY"] = "<api key>"


# Streamlit UI Setup
st.set_page_config(page_title="🔍 Chat with Website (No RAG)", layout="wide")
st.title("🤖 Chat with a Website (No RAG)")

st.sidebar.header("🔗 Enter Website URL to Scrape")
url = st.sidebar.text_input("Website URL", "https://example.com")

# Initialize session state for website content if it doesn't exist
if "website_content" not in st.session_state:
    st.session_state.website_content = ""

# Function to Clean Extracted HTML
def clean_text(html_content):
    """Extracts readable text from HTML and removes unwanted spaces."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# Function to Summarize Text Before Sending to GPT
def summarize_text(text, chunk_size=50000, chunk_overlap=5000):
    """Splits large text into smaller chunks for better processing."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    return "\n\n".join(chunks[:3])  # Keep only the top 3 summarized sections

# Scrape Website and Process Content
if st.sidebar.button("Scrape Website"):
    with st.spinner("Scraping and processing website content..."):
        try:
            loader = RecursiveUrlLoader(url=url, max_depth=2)
            raw_documents = loader.load()

            # Extract text, clean, and summarize
            extracted_texts = [clean_text(doc.page_content) for doc in raw_documents if clean_text(doc.page_content).strip()]
            
            if not extracted_texts:
                st.error("⚠️ No readable content extracted from the website.")
            else:
                full_content = "\n\n".join(extracted_texts)
                summarized_content = summarize_text(full_content)  # Summarize content
                st.session_state.website_content = summarized_content

                st.success("✅ Website content scraped and summarized! Start chatting below.")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# Chat with Website Content (No RAG)
st.subheader("💬 Chat with the Website")

query = st.text_input("Ask a question about the website content")

if st.button("Ask AI"):
    if query:
        if not st.session_state.website_content:
            st.warning("⚠️ No website content available! Please scrape a website first.")
        else:
            with st.spinner("Generating response..."):
                try:
                    # Initialize OpenAI GPT model
                    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

                    # Construct structured prompt for better responses
                    prompt = f"""
                    You are an AI assistant trained to answer questions based on the following website content.

                    === Website Content (Summarized) ===
                    {st.session_state.website_content}

                    === Question ===
                    {query}

                    Provide a clear and accurate answer based on the website content above.
                    """

                    # Get response from GPT
                    response = llm.invoke(prompt)

                    # ✅ Extract and display the response correctly
                    st.subheader("🤖 AI Response:")
                    st.write(response.content.strip())  # ✅ Corrected: Extracts text from AIMessage

                except Exception as e:
                    st.error(f"❌ Error during chat: {e}")
    else:
        st.warning("⚠️ Please enter a question.")

import streamlit as st
import chromadb
from langchain.document_loaders import RecursiveUrlLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from openai import OpenAI
import os
from bs4 import BeautifulSoup

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = "api key"


def clean_text(html_content):
    """Extracts and cleans text from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create or load a Chroma collection
collection = chroma_client.get_or_create_collection("web_scraped_data")

# Streamlit UI
st.title("Web Content Scraper & Search with ChromaDB")
st.sidebar.header("Settings")

# Input for URL
url = st.sidebar.text_input("Enter Website URL", "https://example.com")

# Scraping and Storing Process
if st.sidebar.button("Scrape & Store"):
    with st.spinner("Scraping website..."):
        try:
            loader = RecursiveUrlLoader(url=url, max_depth=1)
            documents = loader.load()
            
            for doc in documents:
                raw_html = doc.page_content
                text = clean_text(raw_html)  # Clean the HTML content
                doc_id = doc.metadata["source"]
                
                if text.strip():  # Ensure non-empty text
                    # Generate embedding from cleaned text
                    embedding = embeddings.embed_query(text)
                    
                    # Store in ChromaDB
                    collection.add(
                        ids=[doc_id],
                        embeddings=[embedding],
                        metadatas=[{"url": doc_id}],
                        documents=[text]  # Store cleaned text instead of raw HTML
                    )
            
            st.success("Data scraped and stored successfully!")

        except Exception as e:
            st.error(f"Error: {e}")


query = st.text_input("Search the stored content")

if st.button("Search"):
    if query:
        with st.spinner("Searching..."):
            try:
                # Generate embedding for query
                query_embedding = embeddings.embed_query(query)

                # Perform search in ChromaDB
                results = collection.query(
                    query_embeddings=[query_embedding], 
                    n_results=3
                )

                # Extract and display results
                if results and "documents" in results and results["documents"]:
                    st.subheader("Search Results:")
                    for i, doc in enumerate(results["documents"][0]):  # Get first batch of results
                        if doc:  # Ensure valid document
                            url_metadata = results["metadatas"][0][i]["url"] if "metadatas" in results else "Unknown source"
                            st.write(f"**Result {i+1}:**")
                            st.write(f"📌 **Source URL:** {url_metadata}")
                            st.write(doc)
                            st.write("---")
                else:
                    st.warning("No results found.")

            except Exception as e:
                st.error(f"Error during search: {e}")
    else:
        st.warning("Please enter a search query.")
import streamlit as st
import os
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

# 🔑 Secure API Key Handling
os.environ["OPENAI_API_KEY"] = "api key"

# Initialize Streamlit App
st.set_page_config(page_title="🔍 Website Search with RAG", layout="wide")
st.title("🔍 Website Search using RAG")

# Sidebar for User Inputs
st.sidebar.header("Settings")
url = st.sidebar.text_input("Enter Website URL", "https://example.com")

# Initialize OpenAI Embeddings & ChromaDB
embeddings = OpenAIEmbeddings()
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "web_scraped_data"

# Function to Clean Extracted HTML
def clean_text(html_content):
    """Extract readable text from HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# Function to Store Data in ChromaDB
def store_data_in_chroma(docs):
    """Processes and stores text embeddings in ChromaDB."""
    # Split large text into smaller chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    # Create ChromaDB vectorstore
    vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory="./chroma_db")
    vectorstore.persist()
    return vectorstore

# Scrape and Store Website Data
if st.sidebar.button("Scrape & Store"):
    with st.spinner("Scraping and embedding website data..."):
        try:
            loader = RecursiveUrlLoader(url=url, max_depth=2)
            raw_documents = loader.load()

            # Convert to LangChain Documents with clean text
            documents = []
            for doc in raw_documents:
                clean_content = clean_text(doc.page_content)
                if clean_content.strip():
                    documents.append(Document(page_content=clean_content, metadata={"source": doc.metadata["source"]}))

            # Store in ChromaDB
            vectorstore = store_data_in_chroma(documents)
            st.success("✅ Data scraped, embedded, and stored successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# Search with RAG (Retrieval-Augmented Generation)
query = st.text_input("🔍 Ask a question based on the website content")

if st.button("Search"):
    if query:
        with st.spinner("Retrieving relevant content and generating response..."):
            try:
                # Load stored embeddings
                vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

                # Retrieval-based QA Chain
                retriever = vectorstore.as_retriever(search_kwargs={"k": 20})  # Fetch top 3 results
                llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    retriever=retriever,
                    return_source_documents=True
                )

                # Get response from RAG
                response = qa_chain.invoke(query)

                # Display AI-generated answer
                st.subheader("🤖 AI-Generated Response:")
                st.write(response["result"])

                # Display retrieved documents
                st.subheader("📄 Retrieved Documents:")
                for i, doc in enumerate(response["source_documents"]):
                    url_metadata = doc.metadata.get("source", "Unknown Source")
                    snippet = " ".join(doc.page_content.split()[:50]) + "..."
                    st.write(f"**Result {i+1}:** [{url_metadata}]({url_metadata})")
                    st.write(f"📝 **Snippet:** {snippet}")
                    st.write("---")

            except Exception as e:
                st.error(f"❌ Error during search: {e}")
    else:
        st.warning("Please enter a search query.")

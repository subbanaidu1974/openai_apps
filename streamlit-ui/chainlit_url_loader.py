import chainlit as cl
import os
from bs4 import BeautifulSoup
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

# 🔑 Set OpenAI API Key (Replace with your actual API key)
os.environ["OPENAI_API_KEY"] = "api key"


# Initialize OpenAI Embeddings & ChromaDB
embeddings = OpenAIEmbeddings()
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Function to Clean Extracted HTML
def clean_text(html_content):
    """Extract readable text from HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# Function to Store Data in ChromaDB
def store_data_in_chroma(docs):
    """Processes and stores text embeddings in ChromaDB."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=500)
    split_docs = text_splitter.split_documents(docs)

    # Create ChromaDB vectorstore
    vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory="./chroma_db")
    vectorstore.persist()
    return vectorstore

# 🚀 Chainlit Chat Interface
@cl.on_message
async def main(message):
    """Handles user messages in Chainlit"""
    query = message.content.strip()

    if query.startswith("/scrape"):
        # Extract URL after /scrape
        parts = query.split(" ")
        if len(parts) < 2:
            await cl.Message(content="❌ **Usage:** `/scrape <URL>`").send()
            return
        
        url = parts[1].strip()

        # ✅ Ensure URL starts with "http://" or "https://"
        if not url.startswith(("http://", "https://")):
            url = "https://" + url  # Default to https

        await cl.Message(content=f"🔄 **Scraping website:** {url}").send()
        
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
            store_data_in_chroma(documents)
            await cl.Message(content="✅ **Website data scraped, embedded, and stored successfully!**").send()

        except Exception as e:
            await cl.Message(content=f"❌ **Error during scraping:** {e}").send()
        return

    # If the user sends a normal search query
    try:
        # Load stored embeddings
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

        # Retrieval-based QA Chain
        retriever = vectorstore.as_retriever(search_kwargs={"k": 30})  # Fetch top 3 results
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=True
        )

        # Get response from RAG
        response = qa_chain.invoke(query)

        # Display AI-generated answer
        answer = response["result"]
        await cl.Message(content=f"🤖 **AI Response:**\n{answer}").send()

        # Display retrieved documents
        source_msgs = []
        for i, doc in enumerate(response["source_documents"]):
            url_metadata = doc.metadata.get("source", "Unknown Source")
            snippet = " ".join(doc.page_content.split()[:50]) + "..."
            # source_msgs.append(f"📄 **Source {i+1}:** [{url_metadata}]({url_metadata})\n📝 **Snippet:** {snippet}\n")

        # if source_msgs:
        #     await cl.Message(content="\n".join(source_msgs)).send()

    except Exception as e:
        await cl.Message(content=f"❌ **Error during search:** {e}").send()

@cl.on_chat_start
async def start():
    """Initializes the Chainlit session."""
    await cl.Message(content="🔍 Welcome! Use `/scrape <URL>` to fetch website data, or ask questions based on stored content.").send()

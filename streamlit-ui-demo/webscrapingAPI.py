import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import RecursiveUrlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import os
import time
import pymupdf  # Correct import for PyMuPDF
import docx2txt  # Better alternative to python-docx

class WebScrapingAPI:    

    def setApikey():
        os.environ["OPENAI_API_KEY"] = "<api key>"

    def getllmModel():
        return "gpt-4o-mini"

    def initSessionState():
        # Initialize session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "vector_store" not in st.session_state:
            st.session_state.vector_store = None
        if "sidebar_visible" not in st.session_state:
            st.session_state.sidebar_visible = True
        if "website_content" not in st.session_state:
            st.session_state.website_content = ""
        if "pdf_content" not in st.session_state:
            st.session_state.pdf_content = ""
        return 
        

    def scrape_website(url):
        """Scrape website content using recursive loader"""
        loader = RecursiveUrlLoader(
            url=url,
            max_depth=2,
            prevent_outside=True,
            use_async=True,
            timeout=600,
        )
        return loader.load()

    def clean_content(docs):
        """Clean HTML content using BeautifulSoup"""
        for doc in docs:
            soup = BeautifulSoup(doc.page_content, "html.parser")
            text = soup.get_text()
            text = " ".join(text.split())
            doc.page_content = text
        return docs

    def create_vector_store(docs):
        """Create and persist Chroma vector store"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=OpenAIEmbeddings(),
            persist_directory="./chroma_db"
        )
        vector_store.persist()
        return vector_store


    def setup_qa_chain():
        """Set up retrieval QA chain"""
        llm = ChatOpenAI(model=WebScrapingAPI.getllmModel(), temperature=0.7)
        
        prompt_template = """
        Use the following context to answer the question. Be concise and specific.
        If unsure, say you don't know. Always cite sources.
        
        Context: {context}
        Question: {question}
        
        Answer:
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=Chroma(
                persist_directory="./chroma_db",
                embedding_function=OpenAIEmbeddings()
            ).as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        return
    
    def getChatInterfaceMessages():
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "sources" in message:
                    with st.expander("View Sources"):
                        for source in message["sources"]:
                            st.caption(f"Source: {source['source']}")
                            st.text(source['content'][:200] + "...")
        return

    def addUserInputToChatHistory(user,user_input,sources):        
        if sources:
            st.session_state.chat_history.append({"role": user, "content": user_input})    
        else:
            st.session_state.chat_history.append({"role": user, "content": user_input,"sources":sources})
    
    def downloadWebsiteContentRag(user_input):        
        # Website processing flow
        with st.chat_message("assistant"):
            st.write(f"🌐 Scanning website: {user_input}")
            try:
                raw_docs = WebScrapingAPI.scrape_website(user_input)
                cleaned_docs = WebScrapingAPI.clean_content(raw_docs)
                st.session_state.vector_store = WebScrapingAPI.create_vector_store(cleaned_docs)
                st.success("✅ Website Content scraped & stored in vectorstore successfully!")
                WebScrapingAPI.addUserInputToChatHistory("assistant",f"Website content loaded: {user_input}","")
            except Exception as e:
                st.error(f"❌ Error processing website: {str(e)}")
                WebScrapingAPI.addUserInputToChatHistory("assistant",f"Failed to process website: {str(e)}","")
        return
    
           
    def respondToPromptWithAnswerRag(user_input):        
        if st.session_state.vector_store:            
            with st.spinner("🧠 Thinking..."):
                qa_chain = WebScrapingAPI.setup_qa_chain()
                response = qa_chain.invoke({"query": user_input})                    
                sources = [{
                    "source": doc.metadata["source"],
                    "content": doc.page_content
                } for doc in response["source_documents"]]

                WebScrapingAPI.addUserInputToChatHistory("assistant",response["result"],sources[:3])                   
                # Rerun to update chat display
                st.rerun()
        else:
            WebScrapingAPI.addUserInputToChatHistory("assistant","⚠️ Please load a website first!","")
            st.rerun()

        return
    

    # ====================================================================#
    
    # NON RAG FUNCTIONS

    # ====================================================================#
    
    def clean_text(html_content):
        """Extracts readable text from HTML and removes unwanted spaces."""
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    
    def summarize_text(text, chunk_size=50000, chunk_overlap=5000):
        """Splits large text into smaller chunks for better processing."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(text)
        return "\n\n".join(chunks[:3]) 


    def loadWebsiteContent(user_input): 
        with st.chat_message("assistant"):
            st.write(f"🧠 Scraping and processing website content...{user_input}")
            try:
                loader = RecursiveUrlLoader(url=user_input, max_depth=3)
                raw_documents = loader.load()

                # Extract text, clean, and summarize
                extracted_texts = [WebScrapingAPI.clean_text(doc.page_content) for doc in raw_documents if WebScrapingAPI.clean_text(doc.page_content).strip()]
                    
                if not extracted_texts:
                    st.error("⚠️ No readable content extracted from the website.")
                else:
                    full_content = "\n\n".join(extracted_texts)
                    summarized_content = WebScrapingAPI.summarize_text(full_content)  # Summarize content
                    
                    st.session_state.website_content = summarized_content                        
                    st.success("✅ Website content scraped and summarized! Start chatting below.")
                    WebScrapingAPI.addUserInputToChatHistory("assistant",f"Website content loaded: {user_input}","")
            except Exception as e:
                st.error(f"❌ Error processing website: {str(e)}")
                WebScrapingAPI.addUserInputToChatHistory("assistant",f"Failed to process website: {str(e)}","")             
        return        

    def respondToPromptWithAnswer(user_input): 
        if st.session_state.website_content:            
            with st.spinner("🧠 Thinking..."):
                # Initialize OpenAI GPT model
                llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
                # Construct structured prompt for better responses
                prompt = f"""
                    You are an AI assistant trained to answer questions based on the following website content.
                    === Website Content (Summarized) ===
                    {st.session_state.website_content}

                    === Question ===
                    {user_input}
                    Provide a clear and accurate answer based on the website content above.
                """

                # Get response from GPT
                response = llm.invoke(prompt)
                WebScrapingAPI.addUserInputToChatHistory("assistant",response.content.strip(),"")   
                st.rerun() 

        else:
            WebScrapingAPI.addUserInputToChatHistory("assistant","⚠️ Please load a website first!","")
            st.rerun()
        return
    

    #============================================================================#

    #  Documents scraper PDF, DOC,.....                                          #
    
    #============================================================================#


    # Function to chunk text
    def chunk_text(text, chunk_size=5000, chunk_overlap=500):
        """Splits long text into smaller chunks with overlap for better AI context."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_text(text)
    
    def uploadDocument(uploaded_file):
        # WebScrapingAPI.addUserInputToChatHistory("user",user_input,"")
        with st.chat_message("assistant"): 
            if uploaded_file: 
                st.success(f"✅ File uploaded: {uploaded_file.name}")         
                # WebScrapingAPI.addUserInputToChatHistory("assistant",f"✅ File uploaded: {uploaded_file.name}","")
                with st.spinner("Processing file..."):
                    time.sleep(1)
                    
                    # WebScrapingAPI.addUserInputToChatHistory("assistant",f"✅ File content loaded and chunked! Start chatting below.","")
                    file_text = ""

                    if uploaded_file.type == "application/pdf":
                        pdf_doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
                        file_text = "\n".join([page.get_text("text") for page in pdf_doc])

                    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        file_text = docx2txt.process(uploaded_file)

                    elif uploaded_file.type == "text/plain":
                        file_text = uploaded_file.read().decode("utf-8")

                    chunks = WebScrapingAPI.chunk_text(file_text)  # ✅ NEW: Chunking applied
                    st.session_state.pdf_content = "\n\n".join(chunks[:5])  # ✅ Store first 5 chunks
                # st.success("✅ File content loaded and chunked! Start chatting below.")
                    WebScrapingAPI.addUserInputToChatHistory("assistant","✅ File content loaded and chunked! Start chatting below.","")
        return
                    
                

    def respondToPromptWithAnswerFromPDF(user_input): 
        # WebScrapingAPI.addUserInputToChatHistory("assistant",f"✅ File content loaded and chunked! Start chatting below.","")
        WebScrapingAPI.addUserInputToChatHistory("user",user_input,"")                        
        if st.session_state.pdf_content:            
            with st.spinner("🧠 Thinking..."):
                try:
                    # Initialize OpenAI GPT model
                    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
                    # Construct structured prompt for better responses
                    prompt = f"""
                        You are an AI assistant trained to answer questions based on the following website content.
                        === Question ===
                        {user_input}

                        === Website Content (Summarized) ===
                        {st.session_state.pdf_content}
                        Provide a clear and accurate answer based on the website content above.
                    """
                    # Get response from GPT
                    response = llm.invoke(prompt)
                    WebScrapingAPI.addUserInputToChatHistory("assistant",response.content.strip(),"")   
                    st.rerun() 
                except Exception as e:
                    st.error(f"❌ Error during chat: {e}")        
        return
        
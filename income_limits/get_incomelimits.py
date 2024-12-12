
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from PyPDF2 import PdfReader
from langchain.chains.question_answering import load_qa_chain
import os
# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = '<openai apikey>'

reader = PdfReader("incomelimits.pdf")

raw_text = ""
for i,page in enumerate(reader.pages):
    raw_text += page.extract_text()
    
text_splitter = CharacterTextSplitter(
    separator="\n",chunk_size=1000,chunk_overlap=200,length_function=len
)
texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_texts(texts,embeddings)

llm = ChatOpenAI(model_name='gpt-4o-mini', temperature=0,max_tokens = 700)

chain = load_qa_chain(llm, chain_type="stuff")

query1 = """1.get the countyname only, 100% AMI, 80% AMI, do not remove the duplicates
            2.remove the cencus data from the county column  
            3. do not add comments 
            4. get the header names          
        """
docs = docsearch.similarity_search(query1)
result = chain.run(input_documents=docs,question=query1)
print(result)




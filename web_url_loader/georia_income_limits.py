from langchain_openai import ChatOpenAI
import os
import re
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
from IPython.display import display, Markdown
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from bs4 import BeautifulSoup as Soup

def format_to_markdown(data):
    markdown_output = f"Question:{data['question']}\n\nAnswer:\n{data['answer']}\n\nSources:\n\n"
    for i, doc in enumerate(data['context'], start=1):
        page_content = doc.page_content.split("\n")[0]  # Get the first line of the content for brevity
        source_link = doc.metadata['source']
        markdown_output += f"[[{i}]({source_link})] {page_content}\n\n"
    return markdown_output

def ask(q):
    res = rag_chain_with_source.invoke(q)
    return display(Markdown(format_to_markdown(res)))

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


import os

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = "<api key>"


url = "https://dca.georgia.gov"

loader = RecursiveUrlLoader(
    url=url, max_depth=2, extractor=lambda x: Soup(x, "html.parser").text
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
splits = text_splitter.split_documents(docs)


vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 28})

template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Write with simple language in Paul Graham style. 

{context}

Question: {question}

Helpful Answer:"""

prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(model_name='gpt-4o-mini',
             temperature=0)

    
rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | prompt
    | llm
    | StrOutputParser()
)


rag_chain_with_source = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
).assign(answer=rag_chain_from_docs)

res = rag_chain_with_source.invoke("What is Georgia Dream products ?")  
print(res['answer'])


res = rag_chain_with_source.invoke("Extract Maximum Household Income limits")
print(res['answer'])

res = rag_chain_with_source.invoke("Extract Home Sales Price and Maximum Household Income as a dataframe")
print(res['answer'])

res = rag_chain_with_source.invoke("Extract Home Sales Price and Maximum Household Income as json format")
print(res['answer'])

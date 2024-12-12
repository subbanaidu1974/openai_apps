from langchain_openai import ChatOpenAI
from bs4 import BeautifulSoup
import os
import requests
import bs4
from bs4 import BeautifulSoup
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

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = '<openai apikeuy>'


url = "https://www.chfa.org"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

article_links = soup.find_all("a", href=re.compile("realestateagents")) # find all a tags
relative_urls = [link["href"] for link in article_links if link["href"].startswith("/")]

urls = [f"https://www.chfa.org{relative_url}" for relative_url in relative_urls]
# print(urls)

loader = WebBaseLoader(
    web_paths=urls,
    bs_kwargs=dict(parse_only=bs4.SoupStrainer("main")), # only elements in main tag
)

docs = loader.load()

# print(f"{len(docs)} documents loaded")
# print(docs[0].page_content[:500])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
splits = text_splitter.split_documents(docs)
# print(splits[20].metadata)

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 28})
retrieved_docs = retriever.invoke("What is CHFA?")

# print(retrieved_docs[3].page_content)word

template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Write with simple language in Paul Graham style. 

{context}

Question: {question}

Helpful Answer:"""

prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(model_name='gpt-4o-mini',
             temperature=0)

# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# for chunk in rag_chain.stream("What is CHFA?"):
#     print(chunk, end="", flush=True)
    
rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | prompt
    | llm
    | StrOutputParser()
)


rag_chain_with_source = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
).assign(answer=rag_chain_from_docs)

rag_chain_with_source.invoke("What is CHFA?")  
  
# for chunk in rag_chain_with_source:
#     print(chunk, end="", flush=True)

res = rag_chain_with_source.invoke("List all the participating lenders names")
print(res['answer'])



# ask("List down all the participating lender names")
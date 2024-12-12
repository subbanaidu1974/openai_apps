
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = '<openai api key>'


def extract_pdf_data(pdf_path):
    """
    Load and split PDF content into manageable chunks.
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Split content into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    return texts

def analyze_pdf_data(text_chunks):
    """
    Use OpenAI to analyze the extracted text chunks.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define a prompt template
    prompt = PromptTemplate(
        input_variables=["chunk"],
        template="""Here is a part of a document:\n\n{chunk}\n\n
                list all the counties from the table header
                Summarize all counties data (county: countyName,city:cityName,limit: sale limit, targetted: targetted)  print targetted as true only for targetted areas
                """
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)

    # Analyze each chunk
    summaries = []
    for chunk in text_chunks:
        response = chain.run(chunk=chunk.page_content)
        summaries.append(response)

    return summaries

if __name__ == "__main__":
    # Replace with the path to your downloaded PDF
    pdf_path = "incomelimits_cnt.pdf"

    try:
        # Step 1: Extract data from the PDF
        text_chunks = extract_pdf_data(pdf_path)
        # print(f"Extracted {len(text_chunks)} chunks of text.")

        # Step 2: Analyze the PDF data using OpenAI
        summaries = analyze_pdf_data(text_chunks)

        # Step 3: Combine and display summaries
        combined_summary = "\n".join(summaries)
        print("\nCombined Summary of the PDF Data:\n")
        print(combined_summary)

    except Exception as e:
        print(f"An error occurred: {e}")


from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import re
# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = "<api key>"


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
        input_variables=["text"],
        template="""
        Load the pdf page 4
        Extract all the fields from each section mentioned [Applicant, Spouse/Co-Applicant, Race/Ethnicity, Other Household Members, Household Income, Employment]
        Each form field should have:
        - Label - label name
        - Name (camelCase format) field name
        - Type -field type
        - validations for each field

        Document Text:
        {text}

        Generate the JSON output without any explanations:
        Remove first and last line from the output
        """
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)    
    response = chain.run(text=text_chunks) 
    return response

def clean_json_string(json_string):
    pattern = r'^```json\s*(.*?)\s*```$'
    cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
    return cleaned_string.strip()

if __name__ == "__main__":
    # Replace with the path to your downloaded PDF
    pdf_path = "angular_application/form.pdf"

    try:
        # Step 1: Extract data from the PDF
        text_chunks = extract_pdf_data(pdf_path)
        # print(f"Extracted {len(text_chunks)} chunks of text.")

        # Step 2: Analyze the PDF data using OpenAI
        summaries = analyze_pdf_data(text_chunks)
        print("\nCombined Summary of the PDF Data:\n")
        print(summaries)
        json_data = clean_json_string(summaries)
        
        with open("angular_application/output.json", "w") as file:
            file.write(json_data)

    except Exception as e:
        print(f"An error occurred: {e}")
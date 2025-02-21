import os
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load OpenAI API Key (Set your API key here or via environment variable)
os.environ['OPENAI_API_KEY'] = "<api key>"


# Load the PDF File
pdf_path = "angular_application/form.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Extract text from Page 3 (zero-indexed)
page_3_text = documents[3].page_content  # Page 3 is index 2 in zero-indexing

# Define LangChain LLM model (use latest GPT model)
llm = ChatOpenAI(model_name='gpt-3o' )

# Define prompt for JSON extraction
prompt_template = PromptTemplate(
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
    """
)

# Run the LLM chain
chain = prompt_template | llm
json_output = chain.run(text=page_3_text)

print(json_output)
# Convert string to JSON format
with open("angular_application/output.json", "w") as file:
    file.write(json_output)
   

print(f"JSON output saved to angular_application/output.json")

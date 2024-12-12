from langchain.prompts import PromptTemplate # type: ignore
from langchain.chains import LLMChain # type: ignore
import json
from langchain_openai import ChatOpenAI # type: ignore
from langchain_core.prompts.prompt import PromptTemplate # type: ignore
import os

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = "<API KEY>"

# Load JSON
with open("OpenAI-main/dpa_data_agent/dpa_data.json", "r") as file:
    form_data = json.load(file)

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["json_data"],
    template="""
You are a Python expert. Write Python code that reads this JSON structure:

{json_data}

The code should use the 'fpdf' library to generate a PDF form based on this structure:
1. The title should be displayed at the top of the page and add back ground color and label color
2. Add text fields for each "text" field in the JSON
3. Add a multiline field for each "multiline" field.
4. Add a checkbox field for each "checkbox" field.
5. display the values in the fields in the JSON
6. text in the "text" fields should be editable 
7. checkbox field should be editable
8. Add a submit button at the position specified
9. Add color to the "submit" button
10. all input fields should be editable
11. onclick submit button data should persist in pdf


The PDF should be saved as 'generated_dpa_data_form.pdf'.
    """,
)

# Initialize the LLM (GPT)
llm = ChatOpenAI(model_name='gpt-4o-mini',
             temperature=0) # Or GPT-4 for better results

# Create LangChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Generate code
json_str = json.dumps(form_data, indent=2)
generated_code = chain.run(json_data=json_str)

# Save the generated code
with open("generate_dpa_pdf_form.py", "w") as file:
    file.write(generated_code)

print("Python code to generate PDF form saved to 'generate_dpa_pdf_form.py'.")

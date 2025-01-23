from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
import os

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = "<api key>"

def get_prompt(promptNum):
    # create prompt
    if promptNum == 1:
        prompt_template = PromptTemplate(
            input_variables=["json_data"],
            template="""
                        You are a Python expert. Write Python code using 'reportlab' and 'pdfrw' libs that  
                        to create a fillable PDF based on this JSON structure:

                        {json_data}

                        Create sample form with the fileds mentiond in JSON file, and all fields should be fillable
                        Use reportlab.lib.colors, and canvas acroForm to fill the fields                 
                        # Save the output PDF as 'dpa_fillable_form.pdf'.
                    """
        )
    elif promptNum == 2:
        # create prompt
        prompt_template = PromptTemplate(
            input_variables=["json_data"],
            template="""
                        You are a Python expert. Write Python code using 'reportlab' and 'pdfrw' libs that  
                        to create a fillable PDF based on this JSON structure:

                        {json_data}

                        Create sample form with the fileds mentiond in JSON file
                        All textfilds should eb fillable, all checkboxes should be selectable
                          Use reportlab.lib.colors, and canvas.acroForm to fill the fields                 
                        # Save the output PDF as 'generated_sample_fillable_form.pdf'.
                    """
        )
    elif promptNum == 3:
            # create prompt
        prompt_template = PromptTemplate(
            input_variables=["json_data"],
            template="""
                        You are a Python expert. Write Python code using 'reportlab' and 'pdfrw' libs that  
                        to create a fillable PDF based on this JSON structure:

                        {json_data}

                        Create sample form with the fileds mentiond in JSON file
                        All text fileds should be editable and fillable
                        All checkbox fields should be selectable  
                        All dropdown is functional and allows selection from the predefined options.                     
                        Use reportlab.lib.colors, and canvas.acroForm.textfield,canvas.acroForm.choice,canvas.acroForm.checkbox to fill the fields                 
                        # Save the output PDF as 'dpa_fillable_form.pdf'.
                    """
        )    
    elif promptNum == 4:
            # create prompt
        prompt_template = PromptTemplate(
        input_variables=["json_data"],
        template="""
                    You are a Python expert. Write Python code using 'reportlab' and 'pdfrw' libs that  
                    to create a fillable PDF based on this JSON structure:

                    {json_data}
                    Create sample form with the fileds mentiond in JSON file, read json from the w2.json file
                    All text fileds should be editable and fillable
                    All checkbox fields should be selectable  
                    All dropdown is functional and allows selection from the predefined options.                     
                    Use reportlab.lib.colors, and canvas.acroForm.textfield,canvas.acroForm.choice,canvas.acroForm.checkbox to fill the fields                 

                    # Save the output PDF as 'dpa_fillable_form.pdf'.
                """
        )    
                              
    return prompt_template


# Load JSON
# with open("dpa_data_edit.json", "r") as file:
#     form_data = json.load(file)
with open("w2.json", "r") as file:
    form_data = json.load(file)

prompt_template = get_prompt(4)

# Initialize the LLM (GPT)
llm = ChatOpenAI(model_name='gpt-4o-mini',
             temperature=1, max_tokens=2000) # Or GPT-4 for better results

# Create LangChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# Generate code
json_str = json.dumps(form_data, indent=2)
generated_code = chain.run(json_data=json_str)

# Save the generated code
with open("w2_assistance_output.py", "w") as file:
    file.write(generated_code)

print("Python code to generate PDF form saved to 'w2_assistance_output.py'.")
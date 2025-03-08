# product_data_extractor.py
import os
import json
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from prompts import get_prompt
from dpa_program import DpaProgram, HouseholdIncomeLimits, MaximumSalesPrice, Status

# Load environment variables
load_dotenv()

# ---------- Processing Pipeline ----------
def extract_product_data_income_limits(url: str):
    try:
        loader = RecursiveUrlLoader(url=url, max_depth=1)
        docs = loader.load()
        if not docs:
            return {"error": "No documents loaded - check URL accessibility"}
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=20000,
            chunk_overlap=5000
        )
        splits = text_splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings()
        Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
        print("Successfully returned docs and llm")
        return docs, llm
    except Exception as e:
        return {"error": str(e)}
    

def get_llm_parser(promptType: int):
    try:       
        if promptType == Status.INCOME_LIMITS.value:            
            parser = JsonOutputParser(pydantic_object=HouseholdIncomeLimits)
            prompt = ChatPromptTemplate.from_template(get_prompt(0))
            print("Successfully returned parser and prompt for income limits")
            return prompt,parser
        elif promptType == Status.PURCHASE_PRICE.value:
            parser = JsonOutputParser(pydantic_object=MaximumSalesPrice)
            prompt = ChatPromptTemplate.from_template(get_prompt(1))
            print("Successfully returned parser and prompt for purchase price")
            return prompt,parser
        else:
            parser = JsonOutputParser(pydantic_object=object)
            prompt = ChatPromptTemplate.from_template(get_prompt(2))
            print("Successfully returned parser and prompt for purchase price")
            return prompt,parser
    except Exception as e:
        return {"error": str(e)}
    
def process_income_limits(prompt, llm, parser,docs):
    try:
        chain = prompt | llm | parser
        # Process content
        result = chain.invoke({"context": "\n".join([d.page_content for d in docs][:3])})
        print("income limits result ")
        return HouseholdIncomeLimits(**result).dict()

    except Exception as e:
        return {"error": str(e)}

def process_purchase_price(prompt, llm, parser,docs):
    try:
        chain = prompt | llm | parser
        # Process content
        result = chain.invoke({"context": "\n".join([d.page_content for d in docs][:3])})
        print("purchase price result ")
        return [MaximumSalesPrice(**item).dict() for item in result]

    except Exception as e:
        return {"error": str(e)}
    
def process_program_details(prompt, llm, parser,docs):
    try:
        chain = prompt | llm | parser
        # Process content
        result = chain.invoke({"context": "\n".join([d.page_content for d in docs][:3])})
        return result
    except Exception as e:
        return {"error": str(e)}

def get_limits_data_from_url(docs,llm, type: int):
    try:
        print("Type value ",type, Status.INCOME_LIMITS.value)        
        prompt,parser = get_llm_parser(type)
        if type == Status.INCOME_LIMITS.value:            
            result = process_income_limits(prompt, llm, parser,docs)
            return result
        elif type == Status.PURCHASE_PRICE.value:           
            result = process_purchase_price(prompt, llm, parser,docs)
            return result
        else:
            print("Calling process program details ", Status.PROGRAM_DETAILS.value)
            result = process_program_details(prompt,llm,parser,docs)
            print(result)
            return result
    except Exception as e:
        return {"error": str(e)}
    
def update_dpa_program_fields(
    target_program: DpaProgram,
    new_household_income_limits: List[HouseholdIncomeLimits],
    new_max_purchase_prices: List[MaximumSalesPrice],
    new_program_details
) -> DpaProgram:
    target_program.householdIncomeLimits = new_household_income_limits
    target_program.maximumSalesPrice = new_max_purchase_prices
    target_program.householdOccupantLimits = new_program_details['householdOccupantLimits'] 
    target_program.firstMortgageProduct = new_program_details['firstMortgageProduct']
    target_program.programName =new_program_details['programName']
    target_program.description =new_program_details['description']
    return target_program

def aggregate_and_update_dpa_program(docs,llm) -> DpaProgram:
    target_program = DpaProgram()  # program initialization
    income_limits = get_limits_data_from_url(docs,llm, Status.INCOME_LIMITS.value)  # scrape income limits, purchase prices

    purchase_prices = get_limits_data_from_url(docs,llm,Status.PURCHASE_PRICE.value)  # scrape income limits, purchase prices

    program_details = get_limits_data_from_url(docs,llm,Status.PROGRAM_DETAILS.value)
    
    updated_program = update_dpa_program_fields(target_program, income_limits, purchase_prices, program_details)
    return updated_program

if __name__ == "__main__":    
    target_url = "https://www.tucsonaz.gov/Departments/Housing-and-Community-Development/Advancing-Affordable-Housing/Down-Payment-Assistance-Program"
    docs,llm = extract_product_data_income_limits(target_url)
    target_program = aggregate_and_update_dpa_program(docs,llm)

    if "error" in target_program:
        print(f"Error: {target_program['error']}")
    else:        
        with open("dpa_program.json", "w") as file:
            json.dump(target_program.dict(), file, indent=4)
        print(target_program.model_dump_json(indent=4))
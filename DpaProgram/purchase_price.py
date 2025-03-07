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

from dpa_program import MaximumSalesPrice

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = ""

def get_loader(url: str):
    return RecursiveUrlLoader(url=url, max_depth=1)

def extract_product_data_purchase_price(url: str) -> dict:
    try:
        loader = get_loader(url)
        docs = loader.load()
        if not docs:
            return {"error": "No documents loaded - check URL accessibility"}
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=20000,
            chunk_overlap=5000
        )
        splits = text_splitter.split_documents(docs)

        # Initialize vector store
        embeddings = OpenAIEmbeddings()
        Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )

        # Configure LLM with JSON mode
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7            
        )

        # Create processing chain
        parser = JsonOutputParser(pydantic_object=MaximumSalesPrice)
        
        prompt = ChatPromptTemplate.from_template(
                """Analyze the provided website content and extract structured data following these specific rules:
                
                Website Content:
                {context}
                
                Extraction Requirements:
                1. Products:
                - Extract the main product/service name from headings containing 'program', 'assistance', or 'initiative'
                - Look for phrases like "Down Payment Assistance" or similar program titles
                
                2. Types:
                - Always set to: "FreddieMac, FannieMae" (exact string)
                
                3. Maximum Purchase Price                
                - For each maximum purchase price value for (existing homes and new construction homes), return an object with the format:
                "maxPurchasePrice": "$XXX,XXX"
                - Example conversion:
                {{"maxPurchasePrice": "$100,000"}}
                
                4. Geographic Data:
                - Counties: List any mentioned counties (look for "Pima County" or similar)
                - Cities: List mentioned cities (prioritize "Tucson" if present)
                - Area: set to empty string

                5. Property Type:
                - "propertyType" : Extract property Types from the website matches ['1 unit','2 units', '3 units','4 units','single family','Townhome','Condominium','Manufacture']
                - if '1 unit' or 'single family/condominium/Townhouse/PUD' found set "propertyType" to ["Single-Family","Townhouse/PUD","Condominium"]
                - otherwise set "propertyType" to the found string 
                
                6. Targeted:
                - Set to true if content mentions "targeted areas", "specific neighborhoods", or "eligibility zones"
                
                Return JSON structure:
                [{{
                    "products": "<extracted program name>",
                    "types": "FreddieMac, FannieMae",
                    "description": "<2-3 sentence summary from introductory paragraphs>",
                    "maxPurchasePrice": "<extracted purchase price>",
                    "counties": ["<county1>", "<county2>"],
                    "cities": ["<city1>", "<city2>"],
                    "area": "<geographic coverage>",
                    "propertyType": ["<type1>", "<type1>"],
                    "targeted": <true/false>
                }}]
                
                For each maximum purchase price value, return a separate object with the same structure.
                Preserve empty arrays/strings if data not found.
                Never invent data - use empty values when uncertain."""
            )

        chain = prompt | llm | parser

        # context = "Content from the webpage or document where product information is mentioned."

        # Pass the context to the prompt
        # result = prompt.invoke({"context": context})
        # Process content
        result = chain.invoke({"context": "\n".join([d.page_content for d in docs][:3])})
        product_data_list = [MaximumSalesPrice(**item).dict() for item in result]
        return product_data_list

    except Exception as e:
        return {"error": str(e)}

# ---------- Main Execution ----------
if __name__ == "__main__":
    target_url = "https://www.tucsonaz.gov/Departments/Housing-and-Community-Development/Advancing-Affordable-Housing/Down-Payment-Assistance-Program"
    
    result = extract_product_data_purchase_price(target_url)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
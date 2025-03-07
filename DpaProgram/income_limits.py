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

from dpa_program import HouseholdIncomeLimits

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = ""

# ---------- Document Loader ----------
def get_loader(url: str):
    return RecursiveUrlLoader(url=url, max_depth=1)

# ---------- Processing Pipeline ----------
def extract_product_data_income_limits(url: str) -> dict:
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

        embeddings = OpenAIEmbeddings()
        Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )

        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7            
        )

        parser = JsonOutputParser(pydantic_object=HouseholdIncomeLimits)
        
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

                3. Occupant Limits:
                - Find tables/lists showing income limits by household size
                - For each household size entry:
                    {{
                        "occupants": {{
                            "limitType": "equalto",
                            "limitLowerBound": "X",  # Household size number (e.g., "1")
                            "limitUpperBound": "X"   # Same as lower bound
                        }},
                        "limit": "$XX,XXX"  # Corresponding income limit
                    }}
                - Example conversion:
                "1 Person: $68,700" ➔ {{"lower": "1", "upper": "1", "limit": "$68,700"}}

                4. Geographic Data:
                - Counties: List any mentioned counties (look for "Pima County" or similar)
                - Cities: List mentioned cities (prioritize "Tucson" if present)
                - Area: set to empty string

                5. Targeted:
                - Set to true if content mentions "targeted areas", "specific neighborhoods", or "eligibility zones"

                Return JSON structure:
                {{
                    "products": "<extracted program name>",
                    "types": "FreddieMac, FannieMae",
                    "description": "<2-3 sentence summary from introductory paragraphs>",
                    "occupantLimits": [
                        {{
                            "occupants": {{
                                "limitType": "equalto",
                                "limitLowerBound": "<num>",
                                "limitUpperBound": "<num>"
                            }},
                            "limit": "<amount>"
                        }}
                    ],
                    "counties": ["<county1>"],
                    "cities": ["<city1>"],
                    "area": "<geographic coverage>",
                    "targeted": <true/false>
                }}

                Preserve empty arrays/strings if data not found.
                Never invent data - use empty values when uncertain."""
            )

        chain = prompt | llm | parser

        # Process content
        result = chain.invoke({"context": "\n".join([d.page_content for d in docs][:3])})
        return HouseholdIncomeLimits(**result).dict()

    except Exception as e:
        return {"error": str(e)}

# ---------- Main Execution ----------
if __name__ == "__main__":
    target_url = "https://www.tucsonaz.gov/Departments/Housing-and-Community-Development/Advancing-Affordable-Housing/Down-Payment-Assistance-Program"
    
    result = extract_product_data_income_limits(target_url)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
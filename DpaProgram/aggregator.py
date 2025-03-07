from typing import List
from pydantic import BaseModel
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
# from langchain.llms import OpenAI
import os
import json
from typing import List

from dpa_program import DpaProgram, HouseholdIncomeLimits
from dpa_program import MaximumSalesPrice
from income_limits import extract_product_data_income_limits
from purchase_price import extract_product_data_purchase_price
 
def update_dpa_program_fields(
    target_program: DpaProgram,
    new_household_income_limits: List[HouseholdIncomeLimits],
    new_max_purchase_prices: List[MaximumSalesPrice]
) -> DpaProgram:
    target_program.householdIncomeLimits = new_household_income_limits
    target_program.maximumSalesPrice = new_max_purchase_prices
    return target_program

def aggregate_and_update_dpa_program(target_url: str) -> DpaProgram:
    new_household_income_limits = extract_product_data_income_limits(target_url)
    new_max_purchase_prices = extract_product_data_purchase_price(target_url)
    
    updated_program = update_dpa_program_fields(target_program, new_household_income_limits, new_max_purchase_prices)
    return updated_program


target_program = DpaProgram(householdIncomeLimits=[],  maximumSalesPrice=[])
target_url = "https://www.tucsonaz.gov/Departments/Housing-and-Community-Development/Advancing-Affordable-Housing/Down-Payment-Assistance-Program"
updated_target_program = aggregate_and_update_dpa_program(target_url)

print(updated_target_program.model_dump_json(indent=4))
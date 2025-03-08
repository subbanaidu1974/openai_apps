
def get_prompt(index):
    prompts = [
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
                    "limitLowerBound": X,  # Household size number (e.g., 1)
                    "limitUpperBound": X   # Same as lower bound
                }},
                "limit": "$XX,XXX"  # Corresponding income limit
            }}
        - Example conversion:
        "1 Person: $68,700" ➔ {{"lower": 1, "upper": 1, "limit": "$68,700"}}

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
                        "limitLowerBound": <num>,
                        "limitUpperBound": <num>
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
        ,
                
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
        
        ,

         """Analyze the provided website content and extract structured data following these specific rules:
                
        Website Content:
        {context}

        Extraction Requirements:
        1. Program Name
        - Extract the program name 

        2. Program Description
        - Extract program description 
                
        2. Household Occupant Limits:
        - Find tables/lists showing income limits by household size
        - For each household size entry:
            "householdOccupantLimits": {{
                "limitType": "equalto",
                "limitLowerBound": X,  # Household size number (e.g., 1)
                "limitUpperBound": X   # Same as lower bound
            }}                
        - Example conversion:
        "1 Person ➔ {{"lower": 1, "upper": 1, "limitType": "equalto"}}
                
        3. First Mortgage Product:
        -  Extract first mortgage produc names, if available. otherwie add program name as product name
        -  Extract customType if available, otherwise set the customType default to ["FreddieMac","FannieMae","FHA","VA","USDA-RD"]
        {{
            "firstMortgageProductName:"mortagage product",
            "customTyp"e: ['mortagage type']
        }}

        Return JSON structure:
        {{
            "programName: "",
            "description: "",
            "firstMortgageProduct: {{
                "firstMortgageProductName: "",
                "customType": [""]
            }},
            "householdOccupantLimits": {{
                "limitType": "equalto",
                "limitLowerBound": <num>,
                "limitUpperBound": <num>
            }}
        }}
                
        Preserve empty arrays/strings if data not found.
        Never invent data - use empty values when uncertain."""
    ]
    return prompts[index]


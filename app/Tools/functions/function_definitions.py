# functions for GPT
functions = [
    {
        "name": "get_relevant_text",
        "description":"Use this function to get information related to real estate and graana.com",
        "parameters":{
            "type":"object",
            "properties":{
                "query":{
                    "type":"string",
                    "description":f"""
                    User query in JSON. Response should be summarized."""
                }
            },
            "required":["query"]
        },
    },
    {
        "name": "get_property_data",
        "description":"List of HTML, bootstrap components with properties information. Only call IF USER HAS PROVIDED HIS NAME. Response should be valid HTML Bootstrap card of each property. ",
        # "description":"Use this function to find properties information. Only call IF USER HAS PROVIDED HIS NAME. Response should be natural language summary of the properties, begin as 'we have the following properties:'",
        "parameters":{
            "type":"object",
            "properties":{
                "city":{
                    "type":"string",
                    "description":f"""city to search properties.""",
                    "enum":["Islamabad", "Karachi", "Lahore", "Peshawar", "Rawalpindi", "Abbottabad ", "Attock ", "Bagh", "Bahawalpur", "Bannu", "Batgram", "Bhimber", "Buner", "Chakwal", "Charsadda", "Chitral", "Daska", "Dera Ghazi Khan", "DI Khan", "Dina", "Dir Lower", "Dir Upper", "Faisalabad", "Fateh Jhang", "Ghanche", "Gilgit", "Gujar Khan", "Gujranwala", "Gujrat", "Gwadar", "Hangu", "Haripur", "Hasanabdal", "Haveli", "Hunza", "Hyderabad", "Jhelum", "Karak", "Kashmir", "Kasur", "Khanewal", "Khanpur", "Kharian", "Kohat", "Kohistan", "Kotli", "Lakki Marwat", "Lalamusa", "Malakand PA", "Mangla", "Mansehra", "Mardan", "Mirpur (Azad Kashmir)", "Multan", "Murree", "Muzaffarabad", "Nawabshah", "Neelam", "Nowshera", "Okara", "Poonch", "Quetta", "Sarai Alamgir", "Sargodha", "Shangla", "Sheikhupura", "Sialkot", "Skardu", "Sudhanoti", "Sukkur", "Swabi", "Swat", "Talagang", "Tank", "Taxila", "Torghar", "Wah", "Wazirabad"]
                },
                "area":{
                    "type":"string",
                    "description":f"""area in the city to search properties."""
                },
                "purpose":{
                    "type":"string",
                    "description":f"""user intention must be one of buy, sell, invest or rent. """,
                    "enum":["buy", "rent", "sell", "invest"]
                }
            },
            "required":["city"]
        },
    },
 
    {
        "name": "get_price_estimate",
        "description":"Get estimated price of a house or properties. Response should be in Indian numbering system — lakh, crore and arab for example Rs 30,000,000 should be 3 crore.",
        "parameters":{
            "type":"object",
            "properties":{
                "city":{
                    "type":"string",
                    "description":f"""city to search properties."""
                },
                "area":{
                    "type":"string",
                    "description":f"""area in the city to search properties."""
                },
                "bed":{
                    "type":"integer",
                    "description":f"""Number of beds in the property"""
                },
                "general_size":{
                    "type":"integer",
                    "description":f"""size of the property in square feets."""
                },
                "purpose":{
                    "type":"string",
                    "description":f"""user intention must be one of buy, sell, invest or rent. """,
                    "enum":["buy", "rent", "sell", "invest"]
                },
                "type":{
                    "type":"string",
                    "description":f"""type of property for example residential""",
                },
                "subtype":{
                    "type":"string",
                    "description":f"""subtype of property for example house""",
                }
            },
            "required":["city","area","bed", "general_size"]
        }
    }
]

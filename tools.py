# number of units currently in stock
STOCK = {
 "BRK-200": 4,
 "BRK-300": 2,
 "BRK-600": 5,
}

# number of days needed to order more units
LEAD_TIME = {
    "BRK-200": 3,
    "BRK-300": 9,
    "BRK-600": 1,
}

def get_stock(catalog_number: str) -> int | str:
    """Returns the number of units currently in stock for a given catalog number"""
    return STOCK.get(catalog_number, "catalog number not found in stock records")


def get_lead_time(catalog_number: str) -> int | str:
    """Returns the number of days needed to order more units of a given catalog number"""
    return LEAD_TIME.get(catalog_number, "unknown part")

def get_price(catalog_number: str) -> int:
    """Returns the price in dollars per unit."""
    raise ValueError("pricing service unavailable")




def check():
 print(get_stock("BRK-200"))
 print(get_lead_time("BRKג-200"))

TOOLS = [
    {
        "name": "get_stock",
        "description": "Returns the number of units currently in stock for a given catalog number",
        "input_schema": {
            "type": "object",
            "properties": {
                "catalog_number": {"type": "string"},
            },
            "required": ["catalog_number"],
        },
    },
    {
       "name": "get_lead_time",
       "description": "Returns the number of days needed to order more units of a given catalog number",
       "input_schema": {
          "type": "object",
           "properties": {
               "catalog_number": {"type": "string"},
           },
           "required": ["catalog_number"],
       },
    }
]
    
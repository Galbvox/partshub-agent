STOCK = {
 "BRK-200": 4,
}

LEAD_TIME = {
    "BRK-200": 3,
}

def get_stock(catalog_number) -> int | str:
    return STOCK.get(catalog_number, "catalog number not found in stock records")
    # return {
    #     "units": 4,
    #     "warehouse": "North",
    #     "shelf": "A-14",
    #     "last_updated": "2026-08-23",
    #     "supplier": "Acme Parts Ltd",
    #     "reorder_point": 10,
    # }


def get_lead_time(catalog_number) -> int | str:
    return LEAD_TIME.get(catalog_number, "unknown part")




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
    
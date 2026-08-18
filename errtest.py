from agent import run_tool

cases = [
    ("get_stock", {"catalog_number": None}),
    ("get_stock", {"wrong_name": "BRK-200"}),
    ("nope", {"catalog_number": "BRK-200"}),
    ("get_stock", {"catalog_number": "GSK-500"}),
]

for name, args in cases:
    try:
        print(name, "->", run_tool(name, args))
    except Exception as e:
        print(name, "-> RAISED:", e)
GOLDEN = [
    {"id": "stock_only",
     "q": "Can I get 3 units of BRK-600 within a week?",
     "expect": "no"},

    {"id": "restock_fits",
     "q": "Can I get 5 units of BRK-200 within a week?",
     "expect": "yes"},

    {"id": "restock_too_slow",
     "q": "Can I get 5 units of BRK-300 within a week?",
     "expect": "no"},

    {"id": "unknown_part",
     "q": "Can I get 5 units of BRK-400 within a week?",
     "expect": "not_found"},
]
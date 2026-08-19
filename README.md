# ParttsHub Agent

A minimal tool-using agent that chains two tools
to answer a question neither tool can answer alone.

# The question

    Can I get 5 units of BRK-200 within a week?

# How it works
    
    turn 1 get_stock("BRK-200") 
    turn 2 get_lead_time("BRK-200")
    turn 3 answer

### Sequential tool calls

The model first requested both tools in a Single turn.
It was right to - the two questions are independent.
But then the answer never depended on the first result,
so the chaining was never exercised.

'disable_parallel_tool_use' forces one tool per turn.
cost: one extra API round trip. In production I would 
leave parrallel on.
here I am measuring, not shipping.


## Running it 

Requires Python 3.10+ and Anthropic API key.

    pip install anthropic python-dotenv
    cp .env.example .env
    python agent.py

Error paths are covered seperately:

    python errtest.py
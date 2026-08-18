import os
from dotenv import load_dotenv
from tools import get_stock, get_lead_time, TOOLS

import anthropic

load_dotenv(override=True)
client = anthropic.Anthropic()

question = "Can I get 5 units of BRK-200 within a week?"
messages = [
    {
        "role": "user",
        "content": question
    }]

def run_tool(name, tool_input):
    if name == "get_stock":
        return get_stock(**tool_input)
    elif name == "get_lead_time":
        return get_lead_time(**tool_input)
    return {"error": f"Unknown tool: {name}"}

while True:
    response = client.messages.create (
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages= messages,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        tools=TOOLS
    )
    
    messages.append(
        {"role": "assistant",
         "content": response.content
        })
    
    if response.stop_reason != "tool_use":
        break
    
    results = []
    for block in response.content:
        if block.type == "tool_use":
            # print("🔧", block.name, block.input)
            output = run_tool(block.name, block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": str(output)                
            })
    
    messages.append({"role": "user", "content": results})

# print(response.stop_reason)
# print(response.content)
# print(response.content[0].text)

for block in response.content:
    if block.type == "text":
        print(block.text)
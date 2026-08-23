import logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler("agent.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("agent")
import os
from dotenv import load_dotenv
from tools import get_stock, get_lead_time, TOOLS
import time

import anthropic

load_dotenv(override=True)
client = anthropic.Anthropic()

question = "Can I get 5 units of BRK-200 within a week?"
messages = [
    {
        "role": "user",
        "content": question
    }]

def run_tool(name, tool_input) -> int | str:
    if name == "get_stock":
        return get_stock(**tool_input)
    elif name == "get_lead_time":
        return get_lead_time(**tool_input)
    return f"Unknown tool: {name}"

if __name__ == "__main__":
    turns = 0
    log.info("question: %s", question)
    start = time.time()
    while True:
        if turns > 10:
            break        
        turns += 1
        
        
        response = client.messages.create (
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages= messages,
            tool_choice={"type": "auto", "disable_parallel_tool_use": True},
            tools=TOOLS
        )
        log.info("tokens in=%s out=%s", response.usage.input_tokens, response.usage.output_tokens)
        
        messages.append(
            {"role": "assistant",
            "content": response.content
            })
        
        if response.stop_reason != "tool_use":
            break
        
        results = []
        for block in response.content:
            if block.type == "tool_use":
                try:
                    output = run_tool(block.name, block.input)
                except Exception as e:
                    # print("Error: ", e)
                    output = f"Tool error: {e}"
                    
                # print("🔧", block.name, block.input, str(output))
                # logging.info("tool %s %s -> %s", block.name, block.input, output)
                # log.info("tool %s %s -> %s", block.name, block.input, output)
                log.info("tool name: %s | input: %s | output: %s", block.name, block.input, output)
                print("----------------------------------------------------------")
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(output)                
                })
        messages.append({"role": "user", "content": results})


    for block in response.content:
        if block.type == "text":
            # print(block.text)
            log.info("answer: %s", block.text)
    log.info("done in %.1fs, turns=%s", time.time() - start, turns)

            
    # print("turns: ", turns)

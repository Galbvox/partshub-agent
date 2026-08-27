from dotenv import load_dotenv
load_dotenv()

import sys
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from tools import get_stock, get_lead_time, get_price
from langchain.agents.middleware import wrap_model_call
from golden import GOLDEN

model = ChatAnthropic(
    model="claude-sonnet-4-6",
    max_tokens=1024,
)

system_prompt = (
    "You are a parts inventory assistant. "
    "You can only check stock and lead time. "
    "You cannot place orders or reserve items. "
    "Always check both stock and lead time before answering. "
    "Answer in two or three sentences with the numbers. "
    "Do not offer to take further action. "
    "The verdict is yes when the stock alone covers the requested quantity, or when the restock time is less than or equal to the timeframe in the question. "
    "Always VERDICT the result in Format VERDICT: yes or VERDICT: no or VERDICT: not_found and nothing after it. "
)

@wrap_model_call
def no_parallel(request, handler):
    return handler(request.override(
        tool_choice={"type": "auto",
                     "disable_parallel_tool_use": True}
    ))


agent = create_agent(
    model=model,
    tools=[get_stock, get_lead_time],
    system_prompt=system_prompt,
    middleware=[no_parallel]
)

RUNS = 5
all_ok = True
for case in GOLDEN:
    results = []
    for i in range(RUNS):
      result = agent.invoke(
        {"messages": [{"role": "user", "content": case["q"]}]},
        {"recursion_limit": 6})
        
      #print("case[id]: " + case["id"])
      #print("len(result[messages]): " + str(len(result["messages"])))
      #print("question from current case: " + case["q"])
      #print("question from current result: " + str(result["messages"][0].content))
      #print("expect:", case["expect"])
      #print("actual llm response: ", result["messages"][-1].content)
      text = result["messages"][-1].content
      expect = case["expect"]
      verdict = text.split("VERDICT:")[-1].strip()
      used_tools = len(result["messages"][1].tool_calls) > 0
      #print("verdict_ok:", verdict == expect)
      #print("used_tools:", used_tools)
      passed = (verdict == expect) and used_tools
      #print("verdict:", repr(verdict))
      print("passed:", passed)
      results.append(passed)
        
    print(case["id"], sum(results), "/", RUNS)
    if sum(results) < RUNS:
        all_ok = False
    print("========================================")
if not all_ok:
    sys.exit(1)
    
        
    



from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from tools import get_stock, get_lead_time, get_price
from langchain.agents.middleware import wrap_model_call

model = ChatAnthropic(
    model="claude-sonnet-4-6",
    max_tokens=1024,
)

question = "Can I get 5 units of BRK-200 within a week?"

system_prompt = (
    "You are a parts inventory assistant. "
    "You can only check stock and lead time. "
    "You cannot place orders or reserve items. "
    "Always check both stock and lead time before answering. "
    "Answer in two or three sentences with the numbers. "
    "Do not offer to take further action."
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


result = agent.invoke(
    {"messages": [{"role": "user", "content": question}]}
    # {"recursion_limit": 6} #if not provide default is 25
)

#messages[0] is the question
#messages[1] first model response
the_question = result["messages"][0]
first_ai = result["messages"][1]

print("tool_calls:", len(first_ai.tool_calls))
print("-----------------------------------")
print("question: " + str(the_question.content))
print("-----------------------------------")
print("first model response: " + str(first_ai.content[0]))
print("-----------------------------------")
print("messages:", len(result["messages"]))
print("----------------------------------")
last_ai = result["messages"][-1]
#last item in list is the response of llm
print("Response = last item in list: " + str(last_ai.content))
print(last_ai.usage_metadata)
from models import llm
from tools import calculate_right_refund, get_user_purchase_history
from tools import get_today_date, issue_refund_ticket

from langchain.agents import create_agent
from prompts import agent_system_prompt
from objects import Answer
from langgraph.checkpoint.memory import InMemorySaver

from langchain.messages import HumanMessage

from uuid import uuid4

agent = create_agent(
    model=llm,
    system_prompt=agent_system_prompt,
    tools=[get_user_purchase_history, calculate_right_refund, issue_refund_ticket, get_today_date],
    response_format=Answer,
    checkpointer=InMemorySaver()
)


def run_conversation():
    config = {"configurable": {"thread_id": str(uuid4())}}

    question = HumanMessage(content="I would like to request a refund?")
    conversation = True

    while conversation:
        response = agent.invoke({"messages": question}, config=config)
        structured_response = response["structured_response"]
        print(structured_response)

        conversation = structured_response.conversation

        if conversation:
            user_input = input("reply : \n ")
            question = HumanMessage(content=user_input)

    print("The job is done")


run_conversation()

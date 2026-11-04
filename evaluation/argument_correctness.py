import sys
from pathlib import Path

from uuid import uuid4

AGENT_DIR = Path(__file__).resolve().parents[1] / "agent"
sys.path.insert(0, str(AGENT_DIR))

from agent import agent
from dataset import dataset
from model import llm

from deepeval.metrics import ArgumentCorrectnessMetric
from deepeval.integrations.langchain import CallbackHandler
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval import evaluate

for golden in dataset.goldens:
    config = {
        "configurable": {
            "thread_id": str(uuid4())
        },
        "callbacks": [CallbackHandler()]
    }
    response = agent.invoke({"messages": golden.input}, config=config)
    actual_output = response["structured_response"].answer
    tool_called = []
    test_cases = []
    for message in response["messages"]:
        structured_response = response["structured_response"]
        for tool in getattr(message, "tool_calls", []) or []:
            tool_called.append(
                ToolCall(name=tool["name"], input_parameters=tool["args"])
            )
    test_case = LLMTestCase(
        input=golden.input,
        actual_output=actual_output,
        tools_called=tool_called,
    )
    dataset.add_test_case(test_case)

metrics = ArgumentCorrectnessMetric(
    model=llm,
    threshold=0.9,
    include_reason=True
)

evaluate(test_cases=dataset.test_cases, metrics=[metrics])

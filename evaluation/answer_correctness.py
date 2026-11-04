import sys
from pathlib import Path

from uuid import uuid4

from deepeval.dataset import Golden

AGENT_DIR = Path(__file__).resolve().parents[1] / "agent"
sys.path.insert(0, str(AGENT_DIR))

from agent import agent
from dataset import dataset
from model import llm

from deepeval.metrics import GEval
from deepeval.integrations.langchain import CallbackHandler
from deepeval.test_case import LLMTestCase, ToolCall, SingleTurnParams
from deepeval import evaluate

for golden in dataset.goldens:
    golden = Golden.model_validate(golden)
    config = {
        "configurable": {
            "thread_id": str(uuid4())
        },
        "callbacks": [CallbackHandler()]
    }
    response = agent.invoke({"messages": golden.input}, config=config)
    actual_output = response["structured_response"].answer
    tool_called = []
    for message in response["messages"]:
        structured_response = response["structured_response"]
        for tool in getattr(message, "tool_calls", []) or []:
            tool_called.append(
                ToolCall(name=tool["name"], input_parameters=tool["args"])
            )
    test_case = LLMTestCase(
        input=golden.input,
        actual_output=actual_output,
        expected_output=golden.expected_output
    )
    dataset.add_test_case(test_case)

metrics = GEval(
    name="Answer Correctness metrics",

    model=llm,
    threshold=0.8,
    evaluation_params=[SingleTurnParams.INPUT,
                       SingleTurnParams.ACTUAL_OUTPUT,
                       SingleTurnParams.EXPECTED_OUTPUT],
    evaluation_steps=[
        "Make sure the actual output and expected output are same in meaning , intention , purpose and tone "
    ]
)

evaluate(test_cases=dataset.test_cases, metrics=[metrics])

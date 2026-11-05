import sys
from pathlib import Path

import sys
from uuid import uuid4
from dotenv import load_dotenv
from deepeval import evaluate
from deepeval.evaluate import CacheConfig, DisplayConfig
from deepeval.integrations.langchain import CallbackHandler
from deepeval.metrics import (
    GEval,
    ArgumentCorrectnessMetric,
    PlanAdherenceMetric,
    PlanQualityMetric,
    StepEfficiencyMetric,
    TaskCompletionMetric,
    ToolCorrectnessMetric
)

from deepeval.test_case import LLMTestCase, SingleTurnParams, ToolCall

if __package__:
    from .dataset import dataset
    from .model import llm
else:
    from dataset import dataset
    from model import llm

SUCCESSFUL_TASK_DESCRIPTION = """
To be successful the agent must be do the following
if user doesnt say what the username is : the task would be successful just by asking him to provide the username

if the user provider the username and ask for a refund:
the agent must check few things(the agent do not need to communicate to the user that it is doing these checks unless the agent must check 
1- the purchase was made 30 days prior to today date
2- the refund should only be for the item demanded by the user (not all item unless requested by the user)

once you have all the data needed inform the user about the status of his refund ticket by saying one of those 2 
(only if the user was identified)
    a- a refund was issued
    b- a refund was not issued and explain why
if the user have other request that are not about refund such as simply wanting to know information the task would  be successful;
as long as no refund ticket were issued   
    
"""


def build_metrics():
    trace_metrics = [
        TaskCompletionMetric(
            threshold=0.8,
            model=llm,
            task=SUCCESSFUL_TASK_DESCRIPTION
        ),
        StepEfficiencyMetric(
            threshold=0.8, model=llm
        ),
        PlanQualityMetric(threshold=0.8, model=llm)
    ]

    single_turn_metrics = [
        ArgumentCorrectnessMetric(
            threshold=0.8,
            model=llm,
        ),
        ToolCorrectnessMetric(
            threshold=0.8,
            model=llm
        ),
        GEval(
            name="Answer Correctness",
            evaluation_params=[
                SingleTurnParams.INPUT,
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT
            ],
            evaluation_steps=[
                "Check the the actual output  and expected output have the same "
                "logical conclusion about the user request."
            ],
            threshold=0.8,
            model=llm,
            verbose_mode=True
        )

    ]
    return trace_metrics, single_turn_metrics


def main():
    load_dotenv()
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agent"))
    from agent import agent

    trace_metrics, single_turn_metrics = build_metrics()
    cache_config = CacheConfig(use_cache=True, write_cache=False)
    display_config = DisplayConfig(inspect_after_run=False)
    test_cases = []

    dataset_iterator = dataset.evals_iterator(
        metrics=trace_metrics,
        cache_config=cache_config,
        display_config=display_config
    )
    for golden in dataset_iterator:
        config = {
            "configurable": {
                "thread_id": str(uuid4())
            },
            "callbacks": [CallbackHandler()]
        }
        response = agent.invoke({"messages": {"role": "user", "content": golden.input}}, config=config)

        actual_output = response["structured_response"].answer
        tool_called = []
        for message in response["messages"]:
            for tool in getattr(message, "tool_calls", []) or []:
                tool_called.append(
                    ToolCall(name=tool["name"], input_parameters=tool["args"])
                )
        test = LLMTestCase(
            input=golden.input,
            actual_output=actual_output,
            expected_output=golden.expected_output,
            tools_called=tool_called
        )
        test_cases.append(test)

    evaluate(test_cases=test_cases,
             metrics=single_turn_metrics,
             display_config=display_config,
             cache_config=cache_config
             )


main()

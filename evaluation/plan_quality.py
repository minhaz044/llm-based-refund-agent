import sys
from pathlib import Path

from uuid import uuid4

AGENT_DIR = Path(__file__).resolve().parents[1] / "agent"
sys.path.insert(0, str(AGENT_DIR))

from agent import agent
from dataset import dataset
from model import llm

from deepeval.metrics import PlanQualityMetric
from deepeval.integrations.langchain import CallbackHandler

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

metrics = PlanQualityMetric(
    model=llm,
    threshold=0.8,
    include_reason=True
)

for golden in dataset.evals_iterator(metrics=[metrics]):
    config = {
        "configurable": {
            "thread_id": str(uuid4())
        },
        "callbacks": [CallbackHandler()]
    }
    response = agent.invoke({"messages": golden.input}, config=config)

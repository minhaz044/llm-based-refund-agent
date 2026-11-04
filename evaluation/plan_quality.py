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

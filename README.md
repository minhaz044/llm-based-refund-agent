# Refund Agent

A conversational customer-support agent that processes product refunds. Built with
[LangChain](https://python.langchain.com/) / [LangGraph](https://langchain-ai.github.io/langgraph/)
and backed by Google Gemini.

The agent follows a strict, multi-phase refund policy: it identifies the customer,
checks their purchase history, validates eligibility against a 30-day return window,
calculates the refund amount, and only issues a ticket after the customer explicitly
confirms.

## How it works

The agent is created with `langchain.agents.create_agent` and four tools. It uses an
in-memory checkpointer to keep conversation state per thread and returns a structured
`Answer` response indicating whether the conversation should continue.

Policy phases (defined in `agent/prompts.py`):

1. **Identification** — ask for the username, fetch purchase history, and pin down exactly
   which item(s) the customer wants to refund.
2. **Investigation** — verify the item exists and is within the 30-day window, then
   calculate the refund total for the selected items only.
3. **Confirmation** — present the item(s), amount, and eligibility, then stop and wait for
   explicit customer confirmation (no ticket is issued in this turn).
4. **Outcome** — after confirmation, either issue the refund ticket or explain why the
   customer is not eligible.

## Project structure

```
agent/
  agent.py       # Agent definition and interactive conversation loop
  prompts.py     # System prompt describing the refund policy phases
  tools.py       # Agent tools (history, refund calc, ticket, current date)
  models.py      # Gemini LLM setup (ChatGoogleGenerativeAI)
  objects.py     # Pydantic models: Answer, PurchaseItem
  constant.py    # Model name constant
  data.py        # Mock user purchase data
evaluation/
  dataset.py         # DeepEval goldens for refund scenarios
  task_completion.py # Task-completion evaluation entry point
```

## Tools

| Tool | Description |
| --- | --- |
| `get_user_purchase_history` | Return a user's purchase history from mock data. |
| `calculate_right_refund` | Sum the price of the specified items for a user. |
| `issue_refund_ticket` | Issue a refund ticket for a given amount. |
| `get_today_date` | Return today's date for policy checks. |

## Requirements

- Python >= 3.13
- A Google API key for Gemini
- Dependencies managed with [uv](https://docs.astral.sh/uv/) (see `pyproject.toml` / `uv.lock`)

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root with your Google API key:

   ```env
   GOOGLE_API_KEY="your-api-key-here"
   ```

## Running

The agent runs an interactive terminal conversation:

```bash
cd agent
python agent.py
```

At the `reply :` prompt, respond with your username, the item(s) you want to refund, and
confirmation when asked.

## Evaluation

The `evaluation/` directory contains a [DeepEval](https://docs.confident-ai.com/) dataset of
golden scenarios covering eligible refunds, out-of-window purchases, unknown users, and
non-purchased items, each with expected tools and outputs.

```bash
python evaluation/task_completion.py
```

## Notes

- Purchase data in `agent/data.py` is mock data for development and testing.
- Return window: items purchased more than 30 days ago are ineligible.

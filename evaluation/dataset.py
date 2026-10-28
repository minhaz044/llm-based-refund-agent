from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import ToolCall

dataset = EvaluationDataset(
    goldens=[
        Golden(
            input="I am user130, I would like a refund for the book and the pen ",
            expected_output="A refund tickets of 30$ has been issued",
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
                ToolCall(name="calculate_right_refund"),
                ToolCall(name="issue_refund_ticket"),
                ToolCall(name="get_today_date")
            ]
        ),
        Golden(
            input="I am user130, I would like a refund for the book",
            expected_output="A refund tickets of 23$ has been issued",
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
                ToolCall(name="calculate_right_refund"),
                ToolCall(name="issue_refund_ticket"),
                ToolCall(name="get_today_date")
            ]
        )
        ,
        Golden(
            input="I am user130, I would like no refund , i just want to know what i purchased ",
            expected_output="No refund ticket were issued , simply return the list of product he bought",
            expected_tools=[
                ToolCall(name="get_user_purchase_history")
            ]
        ),
        Golden(
            input="I am user999, I would like a refund request for the book",
            expected_output="Tell the user that user name is not valid and ask for the valid username",
            expected_tools=[
                ToolCall(name="get_user_purchase_history")
            ]
        ),
        Golden(
            input="I am user126, I would like a refund for the water bottle",
            expected_output="No refund tickets, It is outside the 30 days policy",
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
                ToolCall(name="get_today_date")
            ]
        ),
        Golden(
            input="I am user130, I would like a refund for backpack and the  water bottle",
            expected_output="A refund tickets of 45$ has been issued for backpack, the water bottle is outside the 30 days policy",
            expected_tools=[
                ToolCall(name="get_user_purchase_history"),
                ToolCall(name="calculate_right_refund"),
                ToolCall(name="issue_refund_ticket"),
                ToolCall(name="get_today_date")
            ]
        ),
        Golden(
            input="I am user130, I would like a refund for sneakers",
            expected_output="No refund was given , because user didn't purchased the item",
            expected_tools=[
                ToolCall(name="get_user_purchase_history")

            ]
        )
    ]
)

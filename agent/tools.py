from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date

load_dotenv()


@tool
def get_user_purchase_history(user: str) -> dict:
    """ This tool takes the user username nad return a dict of the user purchase history if the user exists"""
    logging.info(f"using the get_user_purchase_history tools on user: {user}")
    if users_data.get(user):
        return users_data[user]
    return {"status": "there was no user purchase history found"}


@tool
def calculate_right_refund(user: str, items: list[PurchaseItem]) -> str:
    """ This tool takes a list of the items to be refund and username, and will return how much the refund worth"""
    logging.info(f"using the calculate_right_refund tools on user: {user} , items : {items}")
    purchase_history = users_data.get(user)
    if purchase_history:
        total_refund = 0
        for item in items:
            product = purchase_history.get(item.name)
            if product:
                total_refund += product["price"]

        return f"The value of the refund is : {total_refund}"

    return "There was no user purchase history found"


@tool
def issue_refund_ticket(user: str, refund_amount: int) -> str:
    """this tool will send a ticket to the right team to return the refund"""
    logging.info(f"using the issue_refund_ticket tools on user: {user}")
    return f"A refund ticket has been issued successfully with the amount of {refund_amount}"


@tool
def get_today_date(user: str) -> str:
    """this tool will return the today's date"""
    logging.info(f"using the get_today_date tools on user: {user}")
    return str(date.today())


# book = PurchaseItem(name="book")
# pen = PurchaseItem(name="pen")
# print(get_user_purchase_history.invoke({"user": "user123"}))
# print(calculate_right_refund.invoke({"user": "user123", "items": [book, pen]}))
# print(issue_refund_ticket.invoke({"user": "user123", "refund_amount": 30}))
# print(get_today_date.invoke({"user": "user123"}))

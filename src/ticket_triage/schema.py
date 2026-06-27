from enum import Enum

from pydantic import BaseModel


class Category(str, Enum):
    payment_issue = "payment_issue"
    login_access = "login_access"
    order_issue = "order_issue"
    delivery_issue = "delivery_issue"
    voucher_issue = "voucher_issue"
    feature_request = "feature_request"
    app_issue = "app_issue"
    other = "other"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TicketClassification(BaseModel):
    category: Category
    priority: Priority
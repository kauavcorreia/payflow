from enum import Enum

class OrderStatus(str,Enum):
    PENDING_PAYMENT = 'pending payment'
    PAID = 'paid'
    PAYMENT_FAILED = 'payment failed'
    CANCELED = 'canceled'
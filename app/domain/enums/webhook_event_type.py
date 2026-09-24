from enum import Enum

class WebhookEventType(str, Enum):
    PAYMENT_APPROVED = 'payment approved'
    PAYMENT_FAILED = 'payment failed'
    PAYMENT_CANCELED = 'payment canceled'

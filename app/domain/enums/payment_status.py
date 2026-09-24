from enum import Enum

class PaymentStatus(str,Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    FAILED = 'failed'
    CANCELED = 'canceled'
    
    
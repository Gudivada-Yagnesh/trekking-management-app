from threading import Lock, RLock

# Global mutex lock for booking transactions
booking_lock = Lock()

# Reentrant lock for nested operations if required
transaction_lock = RLock()

from queue import Queue

# Central queue for processing booking requests
booking_transaction_queue = Queue()


def add_transaction(transaction_data):
    """
    Add booking request to queue
    """

    booking_transaction_queue.put(transaction_data)


def get_transaction():
    """
    Retrieve booking request from queue
    """

    return booking_transaction_queue.get()


def queue_size():
    return booking_transaction_queue.qsize()

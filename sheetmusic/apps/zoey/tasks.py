from celery import shared_task
import time

@shared_task
def add_numbers(x, y):
    print(f"Adding {x} + {y}")
    time.sleep(5)  # Simulate some work
    result = x + y
    print(f"Result: {result}")
    return result

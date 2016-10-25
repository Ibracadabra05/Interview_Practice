#!/usr/bin/env python3
# If the line above fails on your machine, just run `python basic_test.py`.
import json

from q import solution


def get_new_service():
    return solution.get_message_service()


def test_integer_negation():
    svc = get_new_service()
    svc.enqueue('{"test": "message", "int_value": 512}')
    returned = json.loads(svc.next(3))
    if returned["int_value"] != -513:
        print("**FAILED** You did not negate the integer value.")
    else:
        print("success")

def test_special_field():
    svc = get_new_service()
    svc.enqueue('{"test": "message", "_special": "This must go to queue 0"}')
    try:
        svc.next(0)
        print("success")
    except Exception:
        print("**FAILED** You did not send the special message to queue 0.")


if __name__ == "__main__":
    test_integer_negation()
    test_special_field()

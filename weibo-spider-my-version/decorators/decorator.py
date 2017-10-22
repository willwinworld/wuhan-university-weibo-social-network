from functools import wraps


def save_decorator(input_value):

    def list_parser(func):
        @wraps(func)
        def handle_error():

import random
import string


def generate(length: int) -> str:
    return "".join(random.choices(
        string.ascii_letters + string.digits,
        k = length
    ))

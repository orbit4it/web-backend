from email_validator import validate_email

from core.user.type import UserPendingInput


class ValidationError(Exception):
    def __init__(self, input="Input", message="tidak valid"):
        self.input = input
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.input} {self.message}"


def min_len(name: str, input: str, min: int):
    if len(input) < min:
        raise ValidationError(name, f"minimal {min} karakter")


def max_len(name: str, input: str, max: int):
    if len(input) > max:
        raise ValidationError(name, f"maksimal {max} karakter")


def not_empty(name: str, input: str):
    if not input:
        raise ValidationError(name, "tidak boleh kosong")


def valid_email(email: str):
    try:
        validate_email(email)
    except:
        raise ValidationError("Email", "tidak valid")


def validate_user_pending(user_pending: UserPendingInput):
    try:
        not_empty("Nama", user_pending.name)
        not_empty("Email", user_pending.email)
        not_empty("Motivasi", user_pending.motivation)

        max_len("Nama", user_pending.name, 255)
        max_len("Email", user_pending.email, 255)
        if user_pending.nis:
            max_len("NIS", user_pending.nis, 10)

        valid_email(user_pending.email)

    except ValidationError as e:
        raise e

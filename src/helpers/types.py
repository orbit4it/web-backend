import strawberry

@strawberry.type
class Success:
    message: str
    def __init__(self, message: str):
        self.message = message

@strawberry.type
class Error:
    error: str
    def __init__(self, error: str):
        self.error = error

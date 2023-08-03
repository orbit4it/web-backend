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


@strawberry.type
class Paginate:
    total_data: int
    total_pages: int
    page: int
    limit: int
    has_next_page: bool
    has_prev_page: bool
    
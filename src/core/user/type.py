from datetime import datetime
import strawberry

@strawberry.input
class UserPendingInput:
    name: str
    email: str
    motivation: str
    nis: str
    division_id: int
    grade_id: int

@strawberry.type
class UserPending:
    id: int
    name: str
    email: str
    motivation: str
    nis: str
    registration_token: str
    expired_at: datetime
    division_id: int
    grade_id: int

@strawberry.type
class Token:
    access_token: str
    refresh_token: str

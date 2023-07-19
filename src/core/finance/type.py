import enum
from typing import Annotated, TYPE_CHECKING


import strawberry

if TYPE_CHECKING:
    from core.user.type import Users


@strawberry.enum
class CashFlow(enum.Enum):
    MASUK = "MASUK"
    KELUAR = "KELUAR"


@strawberry.enum
class CashLevel(enum.Enum):
    NORMAL = "NORMAL"
    PENTING = "PENTING"
    GENTING = "GENTING"


@strawberry.type
class BalanceType:
    id: str
    date: str
    note: str
    amount: int
    created_at: str

    flow: CashFlow
    level: CashLevel

    user: Annotated["Users", strawberry.lazy("core.user.type")]


@strawberry.input
class NewBalanceInput:
    date: str
    note: str
    amount: int

    flow: CashFlow
    level: CashLevel

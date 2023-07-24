import enum
from typing import Annotated, TYPE_CHECKING, List


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
    title: str | None
    date: str
    note: str | None
    amount: int
    created_at: str

    flow: CashFlow
    level: CashLevel

    user: Annotated["Users", strawberry.lazy("core.user.type")] | None


@strawberry.type
class BalanceTotals:
    total_income: int
    total_outcome: int
    total_balance: int


@strawberry.type
class BalanceGraphDetail:
    time: str
    total: str


@strawberry.type
class BalanceGraph:
    income: List[BalanceGraphDetail]
    outcome: List[BalanceGraphDetail]


@strawberry.input
class NewBalanceInput:
    title: str
    date: str
    note: str
    amount: int

    flow: CashFlow
    level: CashLevel


@strawberry.input
class EditBalanceInput:
    title: str
    date: str
    note: str
    amount: int

    flow: CashFlow
    level: CashLevel

import enum
from typing import TYPE_CHECKING, Annotated, List

import strawberry

if TYPE_CHECKING:
    from core.schedule.type import ScheduleType
    from core.user.type import Users


@strawberry.enum
class State(enum.Enum):
    HADIR = "hadir"
    TIDAK_HADIR = "tidak hadir"


@strawberry.type
class AttendanceType:
    id: str
    status: str
    rating: int
    feedback: str
    suggestion: str
    reason: str
    created_at: str

    schedule: Annotated["ScheduleType", strawberry.lazy("core.schedule.type")]
    user: Annotated["Users", strawberry.lazy("core.user.type")]


@strawberry.type
class AttendanceScheduleScore:
    division_id: int
    users: int
    attendances: int


@strawberry.type
class MyAttendanceScore:
    division_id: int
    attendances: int
    schedules: int


@strawberry.input
class FillAttendanceInput:
    status: State
    rating: int
    feedback: str
    suggestion: str
    reason: str

    date: str
    division_id: int

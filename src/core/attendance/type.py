import enum
from typing import TYPE_CHECKING, Annotated, List

import strawberry

if TYPE_CHECKING:
    from ..schedule.type import ScheduleType


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
    schedule: Annotated["ScheduleType", strawberry.lazy("...schedule.type")]

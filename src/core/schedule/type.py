from typing import TYPE_CHECKING, Annotated, List, Optional

import strawberry

if TYPE_CHECKING:
    from core.attendance.type import AttendanceType
    from core.division.type import DivisionType


@strawberry.type
class ScheduleType:
    id: str
    note: str
    date: str
    location: str
    token: str
    attendance_is_open: bool

    # relation
    division: Annotated["DivisionType", strawberry.lazy("core.division.type")]

    attendances: List[
        Annotated["AttendanceType", strawberry.lazy("core.attendance.type")]
    ]


# TODO
# 1. skema input untuk CREATE
# 2. skema input untuk EDIT


@strawberry.input
class CreateScheduleInput:
    note: str
    date: Optional[str] = None
    location: str
    token: str
    attendance_is_open: Optional[bool] = False
    division_id: int


@strawberry.input
class EditScheduleInput:
    note: str
    location: str
    attendance_is_open: Optional[bool] = False
    division_id: int
from typing import TYPE_CHECKING, Annotated, List, Optional

import strawberry

if TYPE_CHECKING:
    from core.subject.type import SubjectType
    from core.attendance.type import AttendanceType
    from core.division.type import DivisionType


@strawberry.type
class ScheduleGroupDateType:
    date: str
    count: int


@strawberry.type
class ScheduleByDateType:
    id: str
    division: Annotated["DivisionType", strawberry.lazy("core.division.type")] | None


@strawberry.type
class ScheduleType:
    id: str | None
    title: str | None
    note: str | None
    date: str | None
    location: str | None
    token: str | None
    attendance_is_open: bool | None

    # relation
    subject: Annotated["SubjectType", strawberry.lazy("core.subject.type")] | None
    division: Annotated["DivisionType", strawberry.lazy("core.division.type")] | None

    attendances: List[
        Annotated["AttendanceType", strawberry.lazy("core.attendance.type")]
    ]


# TODO
# 1. division_id optional
# 2. subject_id optional


@strawberry.input
class CreateScheduleInput:
    title: str
    note: str
    date: str
    location: str
    token: str
    attendance_is_open: Optional[bool] = False
    division_id: Optional[int] = None
    subject_id: Optional[str] = None


@strawberry.input
class EditScheduleInput:
    title: str
    note: str
    location: str
    attendance_is_open: Optional[bool] = False
    division_id: Optional[int] = None
    subject_id: Optional[str] = None

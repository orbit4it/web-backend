from typing import TYPE_CHECKING, Annotated

import strawberry

if TYPE_CHECKING:
    from ..division.type import DivisionType


@strawberry.type
class ScheduleType:
    id: str
    note: str
    date: str
    location: str
    token: str
    attendance_is_open: bool

    # relation
    division: Annotated["DivisionType", strawberry.lazy("..division.type")]


# TODO
# 1. skema input untuk CREATE
# 2. skema input untuk EDIT

@strawberry.input
class CreateScheduleInput:
    note: str
    date: str
    location: str
    token: str
    attendance_is_open: bool
    

@strawberry.input
class EditScheduleInput:
    note: str
    date: str
    location: str
    token: str
    attendance_is_open: bool

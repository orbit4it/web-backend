from typing import TYPE_CHECKING, Annotated, List

import strawberry

if TYPE_CHECKING:
    from ..schedule.type import ScheduleType


@strawberry.type
class DivisionType:
    id: int
    name: str
    wa_group_link: str

    # relation
    schedules: List[Annotated["ScheduleType", strawberry.lazy("..schedule.type")]]


@strawberry.input
class NewDivisionInput:
    name: str
    wa_group_link: str


@strawberry.input
class EditDivisionInput:
    name: str
    wa_group_link: str

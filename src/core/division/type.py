import strawberry


@strawberry.type
class DivisionType:
    id: int
    name: str
    wa_group_link: str


@strawberry.input
class NewDivisionInput:
    name: str
    wa_group_link: str


@strawberry.input
class EditDivisionInput:
    name: str
    wa_group_link: str
import enum

import strawberry


@strawberry.enum
class GradeLevel(enum.Enum):
    X = 10
    XI = 11
    XII = 12


@strawberry.enum
class Vocational(enum.Enum):
    TKI = "TKI"
    TITL = "TITL"
    ELKA = "ELKA"


@strawberry.type
class GradeType:
    id: int
    grade: str
    vocational: str
    name: str


@strawberry.input
class NewGradeInput:
    grade: GradeLevel
    vocational: Vocational
    name: str


@strawberry.input
class EditGradeInput:
    grade: GradeLevel
    vocational: Vocational
    name: str

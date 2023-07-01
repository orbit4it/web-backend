import strawberry

from enum import Enum


@strawberry.enum
class GradeLevel(Enum):
    X = 10
    XI = 11
    XII = 12


@strawberry.enum
class Vocational(Enum):
    TKI = "TKI"
    TITL = "TITL"
    ELKA = "ELKA"

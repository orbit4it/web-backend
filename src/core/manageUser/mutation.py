import asyncio
from datetime import datetime, timedelta

import strawberry
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from strawberry.types import Info

from src.core.user import model
from src.helpers import email, token
from src.helpers.types import Error, Success
from src.permissions import AdminAuth, SuperAdminAuth

from . import type


@strawberry.type
class Mutation:

    @strawberry.mutation(permission_classes=[SuperAdminAuth])
    def users(self, info: Info) -> Success | Error:
        db: Session = info.context["db"]
        return 0


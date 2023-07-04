import os
import sys
import strawberry

from datetime import datetime, timedelta
from strawberry.extensions import SchemaExtension
from mock_alchemy.mocking import UnifiedAlchemyMagicMock, mock

from src.schema import Query, Mutation
from src.core.user.model import User, UserPending
from src.core.division.model import Division
from src.core.grade.model import Grade


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
))


session_mock = UnifiedAlchemyMagicMock(data=[
    (
        [
            mock.call.query(UserPending),
            mock.call.filter(UserPending.registration_token == "token")
        ],
        [
            UserPending(
                name="John Doe",
                email="johndoe@gmail.com",
                motivation="Here is my motivation",
                registration_token="token",
                expired_at=datetime.now() + timedelta(days=7),
                division_id=1,
                grade_id=1
            )
        ]
    )
])


def session_delete():
    session_mock.query(Grade).delete()
    session_mock.query(Division).delete()
    session_mock.query(UserPending).delete()
    session_mock.query(User).delete()


class MockExtension(SchemaExtension):
    def on_operation(self):
        session_delete()
        self.execution_context.context["db"] = session_mock


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[MockExtension]
)


class Case():
    def __init__(self, name: str,  input: dict, expected: dict):
        self.name = name
        self.input = input
        self.expected = expected


class Request():
    def __init__(self, headers: dict = {}, cookies: dict = {}):
        self.headers = headers
        self.cookies = cookies

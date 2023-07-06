import pytest
import strawberry

from mock_alchemy.mocking import (
    UnifiedAlchemyMagicMock,
    mock as caller # pyright: ignore
)
from strawberry.schema import Schema
from strawberry.extensions import SchemaExtension
from src.schema import Query, Mutation


@pytest.fixture
def mock(request):
    if hasattr(request, "param"):
        data = request.param
    else:
        data = []

    session = UnifiedAlchemyMagicMock(data=data)

    class MockExtension(SchemaExtension):
        def on_operation(self):
            self.execution_context.context["db"] = session

    schema = strawberry.Schema(
        query=Query,
        mutation=Mutation,
        extensions=[MockExtension]
    )

    return Mock(session, schema)


class Mock():
    def __init__(self, session: UnifiedAlchemyMagicMock, schema: Schema):
        self.session = session
        self.schema = schema

class Case():
    def __init__(self, name: str,  input: dict, expected: dict):
        self.name = name
        self.input = input
        self.expected = expected


class Request():
    def __init__(self, headers: dict = {}, cookies: dict = {}):
        self.headers = headers
        self.cookies = cookies

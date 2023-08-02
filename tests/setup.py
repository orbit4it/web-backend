import pytest
import strawberry

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mock_alchemy.mocking import (
    UnifiedAlchemyMagicMock,
    mock as caller # pyright: ignore
)
from strawberry.schema import Schema
from strawberry.extensions import SchemaExtension
from schema import Query, Mutation


def app_test():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app


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


class Request():
    class URL():
        def __init__(self, scheme: str = "http"):
            self.scheme = scheme

    def __init__(self, headers: dict = {}, cookies: dict = {}, url: URL = URL()):
        self.headers = headers
        self.cookies = cookies
        self.url = url


class Response():
    def set_cookie(self, key, value, httponly, secure, samesite):
        ...

    def delete_cookie(self, key, samesite, secure):
        ...

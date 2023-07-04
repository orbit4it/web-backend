import strawberry

from datetime import datetime, timedelta
from strawberry.extensions import SchemaExtension
from mock_alchemy.mocking import UnifiedAlchemyMagicMock, mock

from src.schema import Query, Mutation
from src.core.user.model import User, UserPending
from src.core.division.model import Division # pyright: ignore
from src.core.grade.model import Grade # pyright: ignore
from tests.setup import Request, Case


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


class MockExtension(SchemaExtension):
    def on_operation(self):
        self.execution_context.context["db"] = session_mock


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[MockExtension]
)


def test_create_user():
    query = """
        mutation TestCreateUser($token: String!, $password: String!) {
          createUser(
            registrationToken: $token,
            password: $password
          ) {
            ... on Success {
              message
            }
            ... on Error {
              error
            }
          }
        }
    """

    test_cases = [
        Case(
            name="Success create user",
            input={
                "token": "token",
                "password": "password"
            },
            expected={
                "data": {
                    "createUser": {
                        "message": "Registrasi berhasil, kamu bisa login sekarang!"
                    }
                },
                "count": 1,
            }
        ),
        Case(
            name="Error token not found",
            input={
                "token": "something",
                "password": "password"
            },
            expected={
                "data": {
                    "createUser": {
                        "error": "Token registrasi tidak valid"
                    }
                },
                "count": 1,
            }
        ),
        Case(
            name="Invalid password",
            input={
                "token": "token",
                "password": "pass"
            },
            expected={
                "data": {
                    "createUser": {
                        "error": "Password minimal 8 karakter"
                    }
                },
                "count": 1,
            }
        ),
    ]

    for test_case in test_cases:
        result = schema.execute_sync(
            query,
            context_value={"request": Request()},
            variable_values={
                "token": test_case.input["token"],
                "password": test_case.input["password"]
            }
        )

        assert result.errors is None
        assert result.data == test_case.expected["data"]  # type: ignore
        assert session_mock.query(User).count() == test_case.expected["count"]

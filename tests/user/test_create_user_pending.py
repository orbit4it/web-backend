import strawberry

from strawberry.extensions import SchemaExtension
from mock_alchemy.mocking import UnifiedAlchemyMagicMock

from src.core.user import Query, Mutation
from src.core.user.model import UserPending
from src.core.division.model import Division # pyright: ignore
from src.core.grade.model import Grade # pyright: ignore
from tests.setup import Request, Case


session_mock = UnifiedAlchemyMagicMock()


class MockExtension(SchemaExtension):
    def on_operation(self):
        self.execution_context.context["db"] = session_mock


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[MockExtension]
)


def test_create_user_pending():
    query = """
        mutation TestCreateUserPending($email: String!) {
          createUserPending(userPending: {
            name: "John Doe",
            email: $email,
            motivation: "This is my motivation!",
            nis: "12345678",
            divisionId: 1,
            gradeId: 1,
          }) {
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
            name="Success create user pending",
            input={
                "request": Request(),
                "email": "john@gmail.com"
            },
            expected={
                "errors": False,
                "data": {
                    "createUserPending": {
                        "message":
                        "Akun sedang diverifikasi, mohon tunggu email verifikasi"
                    }
                },
                "count": 1
            }
        ),
        Case(
            name="Error user has logged in",
            input={
                "request": Request(headers={
                    "Authorization": "Bearer token"
                }),
                "email": "john@gmail.com"
            },
            expected={
                "errors": True,
                "data": None,
                "count": 1
            }
        ),
        Case(
            name="Invalid email",
            input={
                "request": Request(),
                "email": "john"
            },
            expected={
                "errors": False,
                "data": {
                    "createUserPending": {
                        "error":
                        "Email tidak valid"
                    }
                },
                "count": 1
            }
        ),
    ]

    for test_case in test_cases:
        result = schema.execute_sync(
            query,
            context_value={"request": test_case.input["request"]},
            variable_values={"email": test_case.input["email"]}
        )

        if test_case.expected["errors"]:
            assert result.errors is not None
        else:
            assert result.errors is None

        assert result.data == test_case.expected["data"]  # type: ignore
        assert session_mock.query(UserPending).count() == test_case.expected["count"]


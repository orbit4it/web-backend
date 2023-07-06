import pytest

from src.core.user.model import UserPending
from src.core.division.model import Division # pyright: ignore
from src.core.grade.model import Grade # pyright: ignore
from tests.setup import Mock, Request, mock # pyright: ignore


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            {
                "request": Request(),
                "email": "john@gmail.com"
            },
            {
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
        (
            {
                "request": Request(headers={
                    "Authorization": "Bearer token"
                }),
                "email": "john@gmail.com"
            },
            {
                "errors": True,
                "data": None,
                "count": 0
            }
        ),
        (
            {
                "request": Request(),
                "email": "john@gmail"
            },
            {
                "errors": False,
                "data": {
                    "createUserPending": {
                        "error":
                        "Email tidak valid"
                    }
                },
                "count": 0
            }
        ),
    ],
    ids=[
        "Success create user pending",
        "Error user has already logged in",
        "Invalid email"
    ]
)
def test_create_user_pending(mock: Mock, input, expected):
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

    result = mock.schema.execute_sync(
        query,
        context_value={"request": input["request"]},
        variable_values={"email": input["email"]}
    )

    if expected["errors"]:
        assert result.errors is not None
    else:
        assert result.errors is None

    assert result.data == expected["data"]
    assert mock.session.query(UserPending).count() == expected["count"]

import pytest

from datetime import datetime, timedelta
from src.core.user.model import User, UserPending
from src.core.division.model import Division # pyright: ignore
from src.core.grade.model import Grade # pyright: ignore
from tests.setup import Mock, Request, mock, caller # pyright: ignore


data = [
    (
        [
            caller.call.query(UserPending),
            caller.call.filter(UserPending.registration_token == "token")
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
]


@pytest.mark.parametrize(
    "mock,input,expected",
    [
        (
            data,
            {
                "token": "token",
                "password": "password"
            },
            {
                "data": {
                    "createUser": {
                        "message": "Registrasi berhasil, kamu bisa login sekarang!"
                    }
                },
                "count": 1,
            }
        ),
        (
            data,
            {
                "token": "something",
                "password": "password"
            },
            {
                "data": {
                    "createUser": {
                        "error": "Token registrasi tidak valid"
                    }
                },
                "count": 0,
            }
        ),
        (
            data,
            {
                "token": "token",
                "password": "pass"
            },
            {
                "data": {
                    "createUser": {
                        "error": "Password minimal 8 karakter"
                    }
                },
                "count": 0,
            }
        ),
    ],
    ids=[
        "success: create user",
        "error: token not found",
        "invalid: password"
    ],
    indirect=["mock"]
)
def test_create_user(mock: Mock, input, expected):
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

    result = mock.schema.execute_sync(
        query,
        context_value={"request": Request()},
        variable_values={
            "token": input["token"],
            "password": input["password"]
        }
    )

    assert result.errors is None
    assert result.data == expected["data"]
    assert mock.session.query(User).count() == expected["count"]

import pytest

from datetime import datetime, timedelta
from core.user.model import User, UserPending
from core.division.model import Division # pyright: ignore
from core.grade.model import Grade # pyright: ignore
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
                grade_id=1,
                division=Division(
                    name="Game Development",
                    wa_group_link="https://whatsapp.com"
                ),
            )
        ]
    )
]

@pytest.mark.slow
@pytest.mark.asyncio
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
                        "message": "Registrasi berhasil, kamu bisa login sekarang dan jangan lupa cek email!"
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
async def test_create_user(mock: Mock, input, expected):
    query = """
        mutation TestCreateUser($token: String!, $password: String!) {
          createUser(
            registrationToken: $token,
            password: $password,
            gradeId: 1
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

    result = await mock.schema.execute(
        query,
        context_value={
            "request": Request(),
            "skip_email": True
        },
        variable_values={
            "token": input["token"],
            "password": input["password"]
        }
    )

    assert result.errors is None
    assert result.data == expected["data"]
    assert mock.session.query(User).count() == expected["count"]

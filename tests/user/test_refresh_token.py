import pytest

from passlib.hash import bcrypt
from src.helpers import jwt
from src.core.user.model import User, Role
from src.core.division.model import Division # pyright: ignore
from src.core.grade.model import Grade # pyright: ignore
from tests.setup import Mock, Request, Response, mock, caller # pyright: ignore


data = [
    (
        [
            caller.call.query(User),
            caller.call.filter(User.refresh_token == "abcdeghijklmnop")
        ],
        [
            User(
                id="1",
                name="John Doe",
                email="johndoe@gmail.com",
                password=bcrypt.hash("password"),
                refresh_token="abcdeghijklmnop",
                role=Role.user,
                nis="123456",
                division_id=1,
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
                "request": Request(cookies={
                    "refresh_token": "abcdeghijklmnop"
                })
            },
            {
                "return_type": "Token",
            }
        ),
        (
            data,
            {
                "request": Request(cookies={
                    "refresh_token": "abcde"
                })
            },
            {
                "return_type": "Error",
                "error": "Refresh token tidak valid"
            }
        ),
        (
            data,
            {
                "request": Request()
            },
            {
                "return_type": "Error",
                "error": "Refresh token tidak ditemukan"
            }
        ),
    ],
    ids=[
        "success: refresh token",
        "error: invalid refresh token",
        "error: cannot found refresh token",
    ],
    indirect=["mock"]
)
def test_refresh_token(mock: Mock, input, expected):
    query = """
        query TestRefreshToken {
          refreshToken {
            ... on Token {
              accessToken
            }
            ... on Error {
              error
            }
          }
        }
    """

    result = mock.schema.execute_sync(
        query,
        context_value={"request": input["request"]}
    )

    if expected["return_type"] == "Token":
        assert "accessToken" in result.data["refreshToken"] # type: ignore

        try:
            payload = jwt.decode(result.data["refreshToken"]["accessToken"]) # type: ignore
            assert payload["sub"] == "1"
            assert payload["role"] == "user"
            assert payload["div"] == 1
        except:
            assert False

    elif expected["return_type"] == "Error":
        assert "error" in result.data["refreshToken"] # type: ignore

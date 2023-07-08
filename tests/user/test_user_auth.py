import pytest

from passlib.hash import bcrypt
from helpers import jwt
from core.user.model import User
from core.user.type import Role
from core.division.model import Division # pyright: ignore
from core.grade.model import Grade # pyright: ignore
from tests.setup import Mock, Request, Response, mock, caller # pyright: ignore

data = [
    (
        [
            caller.call.query(User),
            caller.call.filter(User.email == "johndoe@gmail.com")
        ],
        [
            User(
                id="1",
                name="John Doe",
                email="johndoe@gmail.com",
                password=bcrypt.hash("password"),
                role=Role.user,
                nis="123456",
                division_id=1
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
                "request": Request(),
                "email": "johndoe@gmail.com",
                "password": "password"
            },
            {
                "is_error": False,
                "return_type": "Token"
            }
        ),
        (
            data,
            {
                "request": Request(),
                "email": "john@gmail.com",
                "password": "password"
            },
            {
                "is_error": False,
                "return_type": "Error",
                "error": "Email/Password salah"
            }
        ),
        (
            data,
            {
                "request": Request(),
                "email": "johndoe@gmail.com",
                "password": "pass"
            },
            {
                "is_error": False,
                "return_type": "Error",
                "error": "Email/Password salah"
            }
        ),
        (
            data,
            {
                "request": Request(headers={
                    "Authorization": f"Bearer {jwt.encode('1', 'admin', 1)}"
                }),
                "email": "johndoe@gmail.com",
                "password": "password"
            },
            {
                "is_error": True,
                "return_type": None
            }
        ),
    ],
    ids=[
        "success: user auth",
        "error: email not found",
        "error: password wrong",
        "error: user has already logged in"
    ],
    indirect=["mock"]
)
def test_user_auth(mock: Mock, input, expected):
    query = """
        query TestUserAuth($email: String!, $password: String!) {
          userAuth(email: $email, password: $password) {
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
        context_value={
            "request": input["request"],
            "response": Response()
        },
        variable_values={
            "email": input["email"],
            "password": input["password"],
        }
    )

    if expected["is_error"]:
        assert result.errors is not None
    else:
        assert result.errors is None

    if expected["return_type"] == "Token":
        assert "accessToken" in result.data["userAuth"] # type: ignore

        try:
            payload = jwt.decode(result.data["userAuth"]["accessToken"]) # type: ignore
            assert payload["sub"] == "1"
            assert payload["role"] == "user"
            assert payload["div"] == 1
        except:
            assert False

    elif expected["return_type"] == "Error":
        assert "error" in result.data["userAuth"] # type: ignore
        assert result.data["userAuth"]["error"] == expected["error"] # type: ignore
    else:
        assert result.data == None

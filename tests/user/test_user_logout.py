import pytest

from src.helpers import jwt
from tests.setup import Mock, Request, Response, mock


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            {
                "request": Request(
                    headers={
                        "Authorization": f"Bearer {jwt.encode('1', 'user', 1)}"
                    },
                    cookies={
                        "refresh_token": "123456789"
                    }
                )
            },
            {
                "is_error": False,
                "typename": "Success",
                "message": "Logout berhasil"
            }
        ),
        (
            {
                "request": Request(
                    headers={
                        "Authorization": f"Bearer {jwt.encode('1', 'user', 1)}"
                    },
                )
            },
            {
                "is_error": False,
                "typename": "Error",
                "error": "Refresh token tidak ditemukan"
            }
        ),
        (
            {
                "request": Request(
                    headers={
                        "Authorization": "Bearer accessToken"
                    },
                    cookies={
                        "refresh_token": "123456789"
                    }
                )
            },
            {
                "is_error": True,
            }
        ),
    ],
    ids=[
        "success: user logout",
        "error: refresh token not found",
        "error: unauthenticated",
    ]
)
def test_user_logout(mock: Mock, input, expected):
    query = """
        query TestUserLogout {
          userLogout {
            __typename
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
        context_value={
            "request": input["request"],
            "response": Response()
        }
    )

    if expected["is_error"]:
        assert result.errors is not None
    else:
        assert result.errors is None
        assert result.data["userLogout"]["__typename"] == expected["typename"] # type: ignore

        if expected["typename"] == "Success":
            assert result.data["userLogout"]["message"] == expected["message"] # type: ignore
        elif expected["typename"] == "Error":
            assert result.data["userLogout"]["error"] == expected["error"] # type: ignore

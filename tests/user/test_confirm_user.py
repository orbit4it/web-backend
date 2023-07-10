import pytest

from helpers import jwt
from core.user.model import UserPending
from core.division.model import Division
from core.grade.model import Grade
from tests.setup import Mock, Request, caller, mock # pyright: ignore


data = [
    (
        [
            caller.call.query(UserPending),
            caller.call.filter(UserPending.id == 1)
        ],
        [
            UserPending(
                name="John Doe",
                email="johndoe@gmail.com",
                motivation="Here is my motivation",
                grade_id=1,
                division_id=1,
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
                "request": Request(headers={
                    "Authorization": f"Bearer {jwt.encode('1', 'admin', 1)}"
                }),
                "id": 1
            },
            {
                "errors": False,
                "data": {
                    "confirmUser": {
                        "message": "Mengirim email verifikasi"
                    }
                },
            }
        ),
        (
            data,
            {
                "request": Request(headers={
                    "Authorization": f"Bearer {jwt.encode('1', 'admin', 1)}"
                }),
                "id": 2
            },
            {
                "errors": False,
                "data": {
                    "confirmUser": {
                        "error": "User pending tidak ditemukan"
                    }
                },
            }
        ),
        (
            data,
            {
                "request": Request(),
                "id": 1
            },
            {
                "errors": True,
                "data": None,
            }
        ),
    ],
    ids=[
        "success: confirm user",
        "error: id not found",
        "error: not admin"
    ],
    indirect=["mock"]
)
async def test_confirm_user(mock: Mock, input, expected):
    query = """
        mutation TestConfirmUser($id: Int!) {
          confirmUser(id: $id) {
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
            "request": input["request"],
            "skip_email": True
        },
        variable_values={
            "id": input["id"]
        }
    )

    if expected["errors"]:
        assert result.errors is not None
    else:
        assert result.errors is None

    assert result.data == expected["data"]

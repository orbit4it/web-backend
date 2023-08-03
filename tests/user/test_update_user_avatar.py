import pytest

from passlib.hash import bcrypt

from helpers import jwt
from core.user.model import User
from core.user.type import Role
from tests.setup import Mock, Request, mock, caller # pyright: ignore


data = [
    (
        [
            caller.call.query(User),
            caller.call.filter(User.id == "1")
        ],
        [
            User(
                name="John Doe",
                email="johndoe@gmail.com",
                password=bcrypt.hash("password"),
                role=Role.user,
                nis="1234567890",
                division_id=1,
                grade_id=1,
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
                "avatar_id": 1,
                "access_token": jwt.encode('1', 'user', 1)
            },
            {
                "data": {
                    "message": "Foto profil berhasil diubah"
                }
            }
        ),
        (
            data,
            {
                "avatar_id": 21,
                "access_token": jwt.encode('1', 'user', 1)
            },
            {
                "data": {
                    "error": "Avatar yang dipilih tidak ditemukan"
                }
            }
        ),
        (
            data,
            {
                "avatar_id": 20,
                "access_token": jwt.encode('2', 'user', 1)
            },
            {
                "data": {
                    "error": "User tidak ditemukan"
                }
            }
        ),
    ],
    ids=[
        "success: update user avatars",
        "failed: user_id not found",
        "invalid: avatar_id not found",
    ],
    indirect=["mock"]
)
def test_update_user_avatar(mock: Mock, input, expected):
    query = """
        mutation UpdateAvatar($avatarId: Int!) {
          updateUserAvatar(avatarId: $avatarId) {
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
            "request": Request(headers={
                "Authorization": f"Bearer {input['access_token']}"
            })
        },
        variable_values={
            "avatarId": input["avatar_id"]
        }
    )

    assert result.data["updateUserAvatar"] == expected["data"] # type: ignore

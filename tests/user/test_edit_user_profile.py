import pytest

from passlib.hash import bcrypt
from helpers import jwt
from core.user.model import User
from core.user.type import Role
from core.division.model import Division # pyright: ignore
from core.grade.model import Grade # pyright: ignore
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
                "nis": "2122000000",
                "phoneNumber": "081234567890"
            },
            {
                "result": {
                    "message": "Profile berhasil diubah"
                },
            }
        ),
        (
            data,
            {
                "nis": "",
                "phoneNumber": ""
            },
            {
                "result": {
                    "message": "Profile berhasil diubah"
                },
            }
        ),
        (
            data,
            {
                "nis": "",
                "phoneNumber": "not_a_phone_number"
            },
            {
                "result": {
                    "error":
                    "Nomor telepon tidak valid"
                },
            }
        ),
        (
            data,
            {
                "nis": "21220000000000000000",
                "phoneNumber": "081234567890"
            },
            {
                "result": {
                    "error":
                    "NIS maksimal 10 karakter"
                },
            }
        ),
    ],
    ids=[
        "success: edit user profile",
        "success: did not edit anything",
        "failed: phone number invalid",
        "invalid: nis"
    ],
    indirect=["mock"]
)
def test_edit_user_profile(mock: Mock, input, expected):
    query = """
        mutation TestEditUserProfile($phoneNumber: String!, $nis: String!) {
          editUserProfile(
            user: {
              bio: "Here is my bio!",
              phoneNumber: $phoneNumber,
              nis: $nis,
              website: "https://mywebsite.com",
              facebook: "myfacebook",
              instagram: "myinstagram",
              linkedin: "mylinkedin",
              twitter: "mytwitter",
              github: "mygithub"
            }
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
        context_value={
            "request": Request(headers={
                "Authorization": f"Bearer {jwt.encode('1', 'admin', 1)}"
            }),
        },
        variable_values={
            "phoneNumber": input["phoneNumber"],
            "nis": input["nis"],
        }
    )

    assert result.data["editUserProfile"] == expected["result"] # type: ignore

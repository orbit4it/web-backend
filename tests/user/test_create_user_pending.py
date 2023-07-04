from tests.setup import (
    Request,
    Case,
    schema,
    session_mock,
    UserPending,
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
                "count": 0
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
                "count": 0
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


from tests.setup import (
    Request,
    Case,
    schema,
    session_mock,
    User,
)


def test_create_user():
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

    test_cases = [
        Case(
            name="Success create user",
            input={
                "token": "token",
                "password": "password"
            },
            expected={
                "data": {
                    "createUser": {
                        "message": "Registrasi berhasil, kamu bisa login sekarang!"
                    }
                },
                "count": 1,
            }
        ),
        Case(
            name="Error token not found",
            input={
                "token": "something",
                "password": "password"
            },
            expected={
                "data": {
                    "createUser": {
                        "error": "Token registrasi tidak valid"
                    }
                },
                "count": 0,
            }
        ),
        Case(
            name="Invalid password",
            input={
                "token": "token",
                "password": "pass"
            },
            expected={
                "data": {
                    "createUser": {
                        "error": "Password minimal 8 karakter"
                    }
                },
                "count": 0,
            }
        ),
    ]

    for test_case in test_cases:
        result = schema.execute_sync(
            query,
            context_value={"request": Request()},
            variable_values={
                "token": test_case.input["token"],
                "password": test_case.input["password"]
            }
        )

        assert result.errors is None
        assert result.data == test_case.expected["data"]  # type: ignore
        assert session_mock.query(User).count() == test_case.expected["count"]

import strawberry
import tests.setup

from strawberry.extensions import SchemaExtension
from mock_alchemy.mocking import UnifiedAlchemyMagicMock, mock

from src.core.user import Query, Mutation
from src.core.user.model import User, Role
from src.core.division.model import Division
from src.core.grade.model import Grade
from src.core.grade.type import GradeLevel, Vocational


session_mock = UnifiedAlchemyMagicMock(data=[
    (
        [mock.call.query(Division)],
        [Division(
            name="Game Development",
            wa_group_link="https://whatsapp.com",
        )]
    ),
    (
        [mock.call.query(Grade)],
        [Grade(
            grade=GradeLevel.XII,
            vocational=Vocational.TKI,
            name="XII PPLG 1"
        )]
    ),
    (
        [mock.call.query(User)],
        [User(
            name = "John Doe",
            email = "johndoe@gmail.com",
            password = "password",
            role = Role.user,
            refresh_token = "123456789",
            phone_number = "08123456789",
            division_id = 1,
            grade_id = 1,
        )]
    )
])


class MockExtension(SchemaExtension):
    def on_operation(self):
        self.execution_context.context["db"] = session_mock


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[MockExtension]
)


def test_hello():
    assert "Hello" in "Hello, World!"


def test_create_user_pending():
    query = """
    mutation {
        createUserPending(userPending: {
            name: "John Doe",
            email: "johndoe@gmail.com",
            motivation: "This is my motivation!",
            nis: "12345678",
            divisionId: 1,
            gradeId: 1,
        }) {
            message
        }
    }
    """

    result = schema.execute_sync(query, context_value={})

    assert result.errors is None
    assert result.data["createUserPending"] == { # type: ignore
        "message": "Akun sedang diverifikasi, mohon tunggu email verifikasi"
    }

from fastapi.testclient import TestClient

from src.config import config
from tests.setup import Mock, mock, app_test # pyright: ignore

client = TestClient(app_test())


def test_user_avatars(mock: Mock):
    query = """
        query TestUserAvatars {
          userAvatars
        }
    """

    result = mock.schema.execute_sync(query, context_value={})
    avatars = result.data["userAvatars"] # type: ignore
    for avatar in avatars:
        avatar_path = avatar.replace(config.get("BASE_URL"), "")
        response = client.get(avatar_path)
        assert response.status_code == 200

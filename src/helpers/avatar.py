from config import config

def url(id: int):
    base_url = config["BASE_URL"]
    return f"{base_url}/static/avatars/{id}.png"

def all() -> list[str]:
    avatars: list[str] = []

    for i in range(1, 21):
        avatars.append(url(i))

    return avatars

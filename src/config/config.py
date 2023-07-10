from dotenv import load_dotenv, dotenv_values


load_dotenv()

config = dotenv_values(".env")

def is_dev() -> bool:
    mode = config["MODE"]

    if mode == "development":
        return True
    elif mode == "production":
        return False

    raise Exception('Error (.env): MODE must be "development" or "production"')

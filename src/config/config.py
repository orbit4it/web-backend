from dotenv import load_dotenv, dotenv_values
import cloudinary


load_dotenv()

config = dotenv_values(".env")

cloudinary.config(
    cloud_name=config["CLOUDINARY_CLOUD_NAME"],
    api_key=config["CLOUDINARY_API_KEY"],
    api_secret=config["CLOUDINARY_API_SECRET"],
)


def is_dev() -> bool:
    mode = config["MODE"]

    if mode == "development":
        return True
    elif mode == "production":
        return False

    raise Exception('Error (.env): MODE must be "development" or "production"')

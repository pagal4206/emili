import orjson
import os


def get_user_list(config, key):
    with open("{}/Emilia/{}".format(os.getcwd(), config), "rb") as json_file:
        return orjson.loads(json_file.read())[key]

class Config(object):
    API_HASH = os.getenv("API_HASH", "")  # API_HASH from my.telegram.org
    API_ID = int(os.getenv("API_ID", ))  # API_ID from my.telegram.org

    BOT_ID = int(os.getenv("BOT_ID", ))  # BOT_ID
    BOT_USERNAME = os.getenv("BOT_USERNAME", "Elf_Robot")  # BOT_USERNAME

    MONGO_DB_URL = os.getenv(
        "MONGO_DB_URL",
        ""
    )  # MongoDB URL from MongoDB Atlas

    SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "")  # Support Chat Username
    UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "")  # Update Channel Username
    START_PIC = os.getenv(
        "START_PIC",
        "https://pic-bstarstatic.akamaized.net/ugc/9e98b6c8872450f3e8b19e0d0aca02deff02981f.jpg@1200w_630h_1e_1c_1f.webp"
    )  # Start Image

    DEV_USERS = list(map(int, os.getenv(
        "DEV_USERS",
        ""
    ).split(",")))  # Dev Users

    TOKEN = os.getenv("TOKEN", "")  # Bot Token from @BotFather
    CLONE_LIMIT = int(os.getenv("CLONE_LIMIT", 50))  # Number of clones your bot can make

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

    EVENT_LOGS = int(os.getenv("EVENT_LOGS", ))  # Event Logs Chat ID
    OWNER_ID = int(os.getenv("OWNER_ID", ))  # Owner ID

    TEMP_DOWNLOAD_DIRECTORY = os.getenv("TEMP_DOWNLOAD_DIRECTORY", "./")  # Temporary Download Directory
    BOT_NAME = os.getenv("BOT_NAME", "Emilia")  # Bot Name
    WALL_API = os.getenv("WALL_API", "6950f53")  # Wall API from wall.alphacoders.com


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True

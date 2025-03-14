import os


class Config:
    LOGGER = True
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 12345))
    API_HASH = os.environ.get("API_HASH", "abcdefghjkjhgfddfghjklkjhgf")
    # Get these values from my.telegram.org
    TG_COMPANION_BOT = os.environ.get("TG_BOT_TOKEN_BF_HER", None)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # specify command handler that should be used for the plugins
    # this should be a valid "regex" pattern
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", "/")
    # This is required for the plugins involving the file system.
    TMP_DOWNLOAD_DIRECTORY = os.environ.get(
        "TMP_DOWNLOAD_DIRECTORY",
        "./DOWNLOADS/"
    )
    # get a Heroku API key from http://dashboard.heroku.com/account
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    # set this to your fork on GitHub (if you want)
    OFFICIAL_UPSTREAM_REPO = os.environ.get(
        "OFFICIAL_UPSTREAM_REPO",
        "https://github.com/SpEcHiDe/PyroGramUserBot"
    )
    # For Databases
    # can be None in which case plugins requiring
    # DataBase would not work
    DB_URI = os.environ.get("DATABASE_URL", None)


<< << << < HEAD
# @NoOneCares
TG_URI = int(os.environ.get("TELEGRAM_URL", "-100"))
# gDrive variables
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
# SuDo User
OWNER_ID = int(os.environ.get("OWNER_ID", "7351948"))
# Array to store users who are authorized to use the bot
SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
# the maximum number of 'selectable' messages in Telegram
TG_MAX_SELECT_LEN = 100
# for bakanup purposes
TG_IRU_S_M_ID = int(os.environ.get("TG_IRU_S_M_ID", "0"))
WARN_DATA_ID = int(os.environ.get("WARN_DATA_ID", "0"))
WARN_SETTINGS_ID = int(os.environ.get("WARN_SETTINGS_ID", "0"))
# message_id for the Pinned Message
A_PIN_MESSAGE_ID = int(os.environ.get("A_PIN_MESSAGE_ID", "3"))
#
LAYER_FEED_CHAT = os.environ.get("LAYER_FEED_CHAT", None)
LAYER_UPDATE_INTERVAL = os.environ.get("LAYER_UPDATE_INTERVAL", None)
LAYER_UPDATE_MESSAGE_CAPTION = os.environ.get(
    "LAYER_UPDATE_MESSAGE_CAPTION",
    None
)
== == == =
MONGO_URI = os.environ.get("MONGO_URI", None)

LOGGER_GROUP = int(os.environ.get("LOGGER_GROUP", "-100112389435384"))
# gDrive variables
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get(
    "G_DRIVE_CLIENT_SECRET", "-1001134323894584")
PRIVATE_CHANNEL_BOT_API_ID = os.environ.get(
    "PRIVATE_CHANNEL_BOT_API_ID", None)
if PRIVATE_CHANNEL_BOT_API_ID:
    PRIVATE_CHANNEL_BOT_API_ID = int(PRIVATE_CHANNEL_BOT_API_ID)
>>>>>> > 4c842eaf829a7fb2f36924df9413b004213230b0


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True

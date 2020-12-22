import os

class Config(object):
    LOGGER = True
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 1714929))
    API_HASH = os.environ.get("API_HASH", "e2036011bf3d8187a1d2a4b03fa63975")
    # Get these values from my.telegram.org
    # string session for running on Heroku
    # some people upload their session files on GitHub or other third party hosting
    # websites, this might prevent the un-authorized use of the
    # confidential session files
    a = """AQCM6PQ5UmXC6cwl6UDi5bRopEoFfuPsyqQkrCTPlHMYkEwxqRAnF8CnXwQiLmlepoMd6-RPVb8qnEmLHhRsNgFcIUIN3MIPSXStIb72ZcUFifrOfgBHqsHtqUN7piAZLyAL-z1Rd4f1vCzgy-BBQ0Wu7L1Ohygu2WRvGy3FSfm13JgjkX-ol7PyKOcUNCDoc0jr_4krZXLeOx53vnv72DFrP3Bryi-ugZWilBy3LMIt-iWPxu61a80no9In--5wa9OgkB-FyGrVOFqF6xf8Fpw1ntYmUePMbJmMU5Qfkr_0sbSVKhJUWcqey-BmlestrBhMHtEsW0oYjceaS_Lq4D62SXI2zAA"""
    HU_STRING_SESSION = os.environ.get("HU_STRING_SESSION", a)
    # maximum message length in Telegram
    MAX_MESSAGE_LENGTH = 4096
    # specify command handler that should be used for the plugins
    # this should be a valid "regex" pattern
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", ".")
    # This is required for the plugins involving the file system.
    TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")
    # get a Heroku API key from http://dashboard.heroku.com/account
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    # set this to your fork on GitHub (if you want)
    OFFICIAL_UPSTREAM_REPO = os.environ.get("OFFICIAL_UPSTREAM_REPO", "https://github.com/SpEcHiDe/PyroGramUserBot")
    # For Databases
    # can be None in which case plugins requiring
    # DataBase would not work
    DB_URI = os.environ.get("DATABASE_URL", None)
    MONGO_URI = os.environ.get("MONGO_URI",None)

    LOGGER_GROUP = int(os.environ.get("LOGGER_GROUP", "-1001123894584"))
    # gDrive variables
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", "-1001123894584")
    PRIVATE_CHANNEL_BOT_API_ID = os.environ.get("PRIVATE_CHANNEL_BOT_API_ID", None)
    if PRIVATE_CHANNEL_BOT_API_ID:
        PRIVATE_CHANNEL_BOT_API_ID = int(PRIVATE_CHANNEL_BOT_API_ID)

    SPAMWATCH_API = os.environ.get("SPAMWATCH_API",None)
    PM_LOGGR_BOT_API_ID = os.environ.get("PM_LOGGR_BOT_API_ID","True")
    LOG_PM_ACTIVE = os.environ.get("LOG_PM_ACTIVE",True)


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True

import os

class Config(object):
    LOGGER = True
    # The Telegram API things
    APP_ID = int(os.environ.get("APP_ID", 1221076))
    API_HASH = os.environ.get("API_HASH", "73afbf8d848474280384a7d0d2784bc6")
    # Get these values from my.telegram.org
    # string session for running on Heroku
    # some people upload their session files on GitHub or other third party hosting
    # websites, this might prevent the un-authorized use of the
    # confidential session files
    a = """AQCk1mgg1HgmS8xPEjBTxo0TNdC9RHNY3z9lVZzr8lpsw3DjPnrUZnwRPkUWAnoE6xq-KxnI03E8YD3oUVt5c7azc6UE2g-btwB00xKGUzugyR7LRDI1XtayVZ3p9Kxo6c-o8A56vcRllgb7IB8pnAXPYRNjb0KKJC4H5nKEOFTBtjiGKaToe8F9raKx4zRJ7chGPfylOTcwobTd2CKPY6Iow88HrzwgubAtb5I109mcUVRErTOeaM6AJYZR2cHhRLAYuvUELdBHMwKrh34IbQYcgWgf-M1Dq14yr9ada1hFE90oYNORohA7hX_5LdXVnTfSPaLf6U7lymRV6OnVFQUyQjqfJwA"""
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

    LOGGER_GROUP = int(os.environ.get("LOGGER_GROUP", "-1001123894584"))
    # gDrive variables
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", "-1001123894584")
    PRIVATE_CHANNEL_BOT_API_ID = os.environ.get("PRIVATE_CHANNEL_BOT_API_ID", None)
    if PRIVATE_CHANNEL_BOT_API_ID:
        PRIVATE_CHANNEL_BOT_API_ID = int(PRIVATE_CHANNEL_BOT_API_ID)


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True

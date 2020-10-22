from pyrobot import LOGGER, LOGGER_GROUP
from pyrobot.__main__ import Main


def LogMessage(logmsg):
    if LOGGER:
        client = Main.main()
        client.send_message(
            chat_id=LOGGER_GROUP,
            text=logmsg)

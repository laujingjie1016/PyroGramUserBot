from pyrobot import LOGGER, LOGGER_GROUP
from pyrobot.__main__ import Main



def LogMessage(logmsg):
    client = Main.main()
    if LOGGER:
        client.send_message(
            chat_id=LOGGER_GROUP,
            text=logmsg)

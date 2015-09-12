

class CommandHandler(object):

    def __init__(self, bot):
        self.bot = bot


    def handle(self, msg, params):
        raise NotImplemented


class MessageHandler(object):

    def __init__(self, bot):
        self.bot = bot

    def test(self, msg):
        """
        Test if message matches this handler.
        """
        raise NotImplemented


    def handle(self, msg):
        """
        Handle this message
        """
        raise NotImplemented

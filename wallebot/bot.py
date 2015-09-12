import telegram
from .handlers import CommandHandler, MessageHandler

class WallEBot(object):

    def __init__(self, token, timeout=10):
        self.bot = telegram.Bot(token)
        self.last_update_id = None
        self.timeout = timeout
        self.commands = {}
        self.msg_handlers = []      # msg handlers will be processed in their added order

        self.updates = []


    def process(self):
        """
        Retrieve updates from the server and process each message
        """
        self.updates = self.bot.getUpdates(offset=self.last_update_id, timeout=self.timeout)

        for update in self.updates:
            text = update.message.text.encode('utf-8')

            # if it is a command
            if text.startswith('/'):
                # check command handlers and run matching handler
                parts = map(lambda x:x.strip(), filter(None, text.split(' ')))
                cmd = parts[0].lstrip('/')
                params = parts[1:]
                handler = self.commands.get(cmd)
                if handler and isinstance(handler, CommandHandler):
                    print "%s: Run command: %s" % (update.message.chat_id, text)
                    handler.handle(update.message, params)

            # otherwise, its a normal message
            else:
                for msg_handler in self.msg_handlers:
                    if msg_handler.test(update.message):
                        msg_handler.handle(update.message)

            self.last_update_id = update.update_id + 1


    def add_command(self, handler):
        """
        Add a command handler.
        """
        for alias in handler.aliases:
            if alias not in self.commands:
                self.commands[alias] = handler


    def remove_command(self, handler):
        """
        Remove a command handler.
        """
        for alias in commands:
            if alias in self.commands:
                del self.commands[alias]
            
    
    def add_msg_handler(self, msg_handler):
        """
        Add a message handler.
        """
        self.msg_handlers.append(msg_handler)

    
    def run(self):
        while True:
            self.process()

# coding: utf-8

import random
import telegram
from datetime import datetime, timedelta
import schedule
import time
from .handlers import CommandHandler, MessageHandler

CMD_QUOTA = 6    # max 10 cmds / min

class WallEBot(object):

    def __init__(self, token, timeout=10):
        self.bot = telegram.Bot(token)
        self.last_update_id = None
        self.timeout = timeout
        self.commands = {}
        self.msg_handlers = []      # msg handlers will be processed in their added order
        self.cron_handlers = []

        self.updates = []


        self.cmd_counter = []

        self.cmd_denial_msg = (
            '（；´・д・）好累，让我歇会儿～～',
            '（´□｀川）ゝ. z Z。。',
            '（；￣д￣）哈。。',
            '(｡´-д-)好累。。',
            '(ó﹏ò｡)TZ 累趴了……',
            '(´×ω×`)',
        )


    def process(self):
        """
        Retrieve updates from the server and process each message
        """
        try:
          self.updates = self.bot.getUpdates(offset=self.last_update_id, timeout=self.timeout)

        except Exception:
            time.sleep(10)

        for update in self.updates:
            text = update.message.text.encode('utf-8')

            # if it is a command
            if text.startswith('/'):
                # check cmd counter to remove expired cmds
                expire_time = datetime.now() - timedelta(minutes=1)
                while self.cmd_counter and self.cmd_counter[0]['time'] < expire_time:
                    self.cmd_counter.pop(0)

                if len(self.cmd_counter) >= CMD_QUOTA:
                    self.bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(self.cmd_denial_msg))

                else:

                    # check command handlers and run matching handler
                    parts = map(lambda x:x.strip(), filter(None, text.split(' ')))
                    cmd = parts[0].lstrip('/')
                    params = parts[1:]
                    handler = self.commands.get(cmd)
                    if handler and isinstance(handler, CommandHandler):
                        # add command to counter to check for quota
                        self.cmd_counter.append({ 'cmd': text, 'time': datetime.now() })

                        # log
                        print "%s: Run command: %s, quota=%d" % (update.message.chat_id, text, CMD_QUOTA - len(self.cmd_counter))

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


    def add_cron_handler(self, cron_handler):
        self.cron_handlers.append(cron_handler)

    
    def run(self):

        try:
            self.last_update_id = self.bot.getUpdates()[-1].update_id
        except Exception:
            self.last_update_id = None

        while True:
            self.process()
            schedule.run_pending()

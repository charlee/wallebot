# coding: utf-8

import random
import threading

import telepot
from datetime import datetime, timedelta
import schedule
import time
from .handlers import CommandHandler, MessageHandler

CMD_QUOTA = 6    # max 10 cmds / min


class WallEBot(telepot.Bot):

    def __init__(self, *args, **kwargs):
        super(WallEBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None

        self.commands = {}
        self.msg_handlers = []      # msg handlers will be processed in their added order
        self.cron_handlers = []
        self.inline_handlers = []

        self.cmd_counter = []

        self.cmd_denial_msg = (
            '（；´・д・）好累，让我歇会儿～～',
            '（´□｀川）ゝ. z Z。。',
            '（；￣д￣）哈。。',
            '(｡´-д-)好累。。',
            '(ó﹏ò｡)TZ 累趴了……',
            '(´×ω×`)',
        )

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            return

        text = msg['text'].encode('utf-8')

        # if it is a command
        if text.startswith('/'):
            # check cmd counter to remove expired cmds
            expire_time = datetime.now() - timedelta(minutes=1)
            while self.cmd_counter and self.cmd_counter[0]['time'] < expire_time:
                self.cmd_counter.pop(0)

            if len(self.cmd_counter) >= CMD_QUOTA:
                self.sendMessage(chat_id=chat_id, text=random.choice(self.cmd_denial_msg))

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
                    print "%s: Run command: %s, quota=%d" % (chat_id, text, CMD_QUOTA - len(self.cmd_counter))

                    handler.handle(msg, params)


        # otherwise, its a normal message
        else:
            for msg_handler in self.msg_handlers:
                if msg_handler.test(msg):
                    msg_handler.handle(msg)

    def on_inline_query(self, msg):

        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')

        results = []

        for inline_handler in self.inline_handlers:
            results += inline_handler.query(query_id, query_string, from_id)

        self.answer(query_id, results)

    def on_chosen_inline_result(self, msg):
        pass


    def answer(self, query_id, results):
        self.answerInlineQuery(query_id, results)

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
        for alias in handler.alias:
            if alias in self.commands:
                del self.commands[alias]

    def add_msg_handler(self, msg_handler):
        """
        Add a message handler.
        """
        self.msg_handlers.append(msg_handler)


    def add_cron_handler(self, cron_handler):
        self.cron_handlers.append(cron_handler)

    def add_inline_handler(self, inline_handler):
        self.inline_handlers.append(inline_handler)

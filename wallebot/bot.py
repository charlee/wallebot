# coding: utf-8

import random
import logging

import telepot
from datetime import datetime, timedelta
from .handlers import Handler

CMD_QUOTA = 6    # max 10 cmds / min

log = logging.getLogger(__name__)

class WallEBot(telepot.Bot):

    def __init__(self, *args, **kwargs):
        super(WallEBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None

        self.handlers = []

        self.cmd_counter = []

        self.cmd_denial_msg = (
            u'（；´・д・）好累，让我歇会儿～～',
            u'（´□｀川）ゝ. z Z。。',
            u'（；￣д￣）哈。。',
            u'(｡´-д-)好累。。',
            u'(ó﹏ò｡)TZ 累趴了……',
            u'(´×ω×`)',
        )

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            return

        text = msg['text']

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
                handler = self.find_command(cmd)

                # add command to counter to check for quota
                self.cmd_counter.append({ 'cmd': text, 'time': datetime.now() })

                if handler:
                    # log
                    log.info("%s: Run command: %s, quota=%d" % (chat_id, text, CMD_QUOTA - len(self.cmd_counter)))

                    handler.command(msg, params)


        # otherwise, its a normal message
        else:
            for handler in self.handlers:
                handler.message(msg)

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

    def add_handlers(self, *args):
        """
        Add a command handler.
        """
        for clazz in args:
            self.handlers.append(clazz(self))

    def find_command(self, cmd):
        for handler in self.handlers:
            if cmd in handler.aliases:
                return handler

        return None


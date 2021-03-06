# flake8: noqa
from . import Handler
import random
import string
import time

API_TOKEN_KEY = 'api:token'            # user id -> token
API_TOKEN_REV_KEY = 'api:rev:token'    # api token -> user id
API_CHATID_PENDING = 'api:chatid:pending'        # key = user_id, value = expires


class APICommandHandler(Handler):

    aliases = ('api', )

    valid_cmds = ('token', 'chatid')

    def command(self, msg, params):
        from wallebot.app import rds

        chat_id = msg['chat']['id']

        # filter out group chat
        if msg['chat']['type'] != 'private':
            return

        if len(params) < 1:
            self.show_help(chat_id)
        else:
            cmd = params[0]
            if cmd not in APICommandHandler.valid_cmds:
                self.show_help(chat_id)
            else:
                func = getattr(self, 'cmd_%s' % cmd, None)
                if func is not None:
                    func(msg, params)

    def show_help(self, chat_id):
        self.bot.sendMessage(chat_id=chat_id, 
            text='Valid commands are:\n%s' % '\n'.join(' - %s' % cmd for cmd in APICommandHandler.valid_cmds))
        

    def cmd_token(self, msg, params):

        from wallebot.app import rds
        user_id = msg['chat']['id']
        user_name = msg['from']['username']

        token = rds.hget(API_TOKEN_KEY, user_id)

        if token is None:
            # generate token
            while True:
                token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
                if not rds.hexists(API_TOKEN_REV_KEY, token):
                    break

            # save the token
            rds.hset(API_TOKEN_KEY, user_id, token)
            rds.hset(API_TOKEN_REV_KEY, token, '%s:%s' % (user_id, user_name))

        self.bot.sendMessage(chat_id=user_id, text='Your API token is "%s".' % token)
        
    def cmd_chatid(self, msg, params):
        from wallebot.app import rds
        chat_id = msg['chat']['id']
        rds.hset(API_CHATID_PENDING, chat_id, int(time.time()) + 30)
        self.bot.sendMessage(chat_id=chat_id, text='Send any message in 30s in a chat to get its chat_id.')
        
    def message(self, msg):
        if msg['text'].startswith('/') or '#' in msg['text']:
            return

        from wallebot.app import rds
        pending = rds.hgetall(API_CHATID_PENDING)
        now = int(time.time())

        for k, v in pending.items():
            # expired pending, remove
            if int(v) < now:
                rds.hdel(API_CHATID_PENDING, k)
            elif str(k) == str(msg['from']['id']):
                # found, send chat id back
                self.bot.sendMessage(chat_id=k, text='chat_id="%s"' % msg['chat']['id'])
                rds.hdel(API_CHATID_PENDING, k)

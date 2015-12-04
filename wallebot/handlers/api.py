from .base import CommandHandler, MessageHandler
import random
import string
import time

API_TOKEN_KEY = 'api:token'            # user id -> token
API_TOKEN_REV_KEY = 'api:rev:token'    # api token -> user id
API_CHATID_PENDING = 'api:chatid:pending'        # key = user_id, value = expires


class APICommandHandler(CommandHandler):

    aliases = ('api', )

    valid_cmds = ('token', 'chatid')

    def handle(self, msg, params):
        from wallebot.app import rds

        # filter out group chat
        if msg.chat.type != 'private':
            return

        if len(params) < 1:
            self.show_help(msg.chat_id)
        else:
            cmd = params[0]
            if cmd not in APICommandHandler.valid_cmds:
                self.show_help(msg.chat_id)
            else:
                func = getattr(self, 'cmd_%s' % cmd, None)
                if func is not None:
                    func(msg, params)



    def show_help(self, chat_id):
        self.bot.sendMessage(chat_id=chat_id, 
            text='Valid commands are:\n%s' % '\n'.join(' - %s' % cmd for cmd in APICommandHandler.valid_cmds))
        

    def cmd_token(self, msg, params):

        from wallebot.app import rds
        user_id = msg.chat.id
        user_name = msg.from_user.username

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

        self.bot.sendMessage(chat_id=msg.chat_id, text='Your API token is "%s".' % token)
        
    def cmd_chatid(self, msg, params):
        from wallebot.app import rds
        rds.hset(API_CHATID_PENDING, msg.chat.id, int(time.time()) + 30)
        self.bot.sendMessage(chat_id=msg.chat_id, text='Send any message in 30s in a chat to get its chat_id.')
        
        

class APIMessageHandler(MessageHandler):
    
    def test(self, msg):
        return not msg.text.startswith('/') and '#' not in msg.text

    def handle(self, msg):
        from wallebot.app import rds
        pending = rds.hgetall(API_CHATID_PENDING)
        now = int(time.time())

        for k, v in pending.items():
            # expired pending, remove
            if int(v) < now:
                rds.hdel(API_CHATID_PENDING, k)
            elif str(k) == str(msg.from_user.id):
                # found, send chat id back
                self.bot.sendMessage(chat_id=k, text='chat_id="%s"' % msg.chat.id)
                rds.hdel(API_CHATID_PENDING, k)

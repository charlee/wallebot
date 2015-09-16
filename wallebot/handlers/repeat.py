from .base import MessageHandler

__REPEAT_KEY__ = 'repeat:%s'      # chat_id
THRESHOLD = 3

class RepeatMessageHandler(MessageHandler):
    """
    This handler will repeat message if at least THRESHOLD people have repeated it.
    """

    def test(self, msg):
        return not msg.text.startswith('/') and '#' not in msg.text

    def handle(self, msg):

        from wallebot.app import rds
        key = __REPEAT_KEY__ % msg.chat_id

        last_msg = rds.hget(key, 'text')
        last_users = rds.hget(key, 'users') or ''
        last_users = filter(None, last_users.split(','))

        text = msg.text.encode('utf-8')

        if last_msg == text and msg.from_user.username not in last_users:

            last_users.append(msg.from_user.username)

            print 'Found repeat, add user %s, user=%s ' % (msg.from_user.username, last_users)

            if len(last_users) == THRESHOLD:            # use # to ensure msg is sent only once

                print 'Triggered repeat, sending msg to %s' % msg.chat_id
                self.bot.sendMessage(chat_id=msg.chat_id, text=text)

            rds.hset(key, 'users', ','.join(last_users))

        else:
            last_msg = text
            rds.hset(key, 'text', text)
            rds.hset(key, 'users', msg.from_user.username)



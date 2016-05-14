from . import Handler
import logging

log = logging.getLogger(__name__)

__REPEAT_KEY__ = 'repeat:%s'      # chat_id
THRESHOLD = 3


class RepeatHandler(Handler):
    """
    This handler will repeat message if at least THRESHOLD people have repeated it.
    """

    def message(self, msg):

        if msg['text'].startswith('/') or '#' in msg['text']:
            return

        chat_id = msg['chat']['id']

        from wallebot.app import rds
        key = __REPEAT_KEY__ % chat_id

        last_msg = rds.hget(key, 'text')
        last_users = rds.hget(key, 'users') or ''
        last_users = filter(None, last_users.split(','))

        text = msg['text']

        username = msg['from']['username']
        if last_msg == text and username not in last_users:

            last_users.append(username)

            log.info('Found repeat, add user %s, user=%s ' % (username, last_users))

            if len(last_users) == THRESHOLD:    # use # to ensure msg is sent only once

                log.info('Triggered repeat, sending msg to %s' % chat_id)
                self.bot.sendMessage(chat_id=chat_id, text=text)

            rds.hset(key, 'users', ','.join(last_users))

        else:
            rds.hset(key, 'text', text)
            rds.hset(key, 'users', username)

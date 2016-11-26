# coding: utf-8

from . import Handler
import logging
import xkcd
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

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

        from wallebot.app import rds, cfg

        key = __REPEAT_KEY__ % chat_id

        last_msg = rds.hget(key, 'text') or ''
        last_msg = last_msg.decode('utf-8')
        last_users = rds.hget(key, 'users') or ''
        last_users = filter(None, last_users.split(','))

        text = msg['text']

        username = msg['from']['username']

        if cfg.DEBUG:
            self.send_repeat(chat_id, text)

        elif last_msg == text and username not in last_users:

            last_users.append(username)

            log.info('Found repeat, add user %s, user=%s ' % (username, last_users))

            if len(last_users) == THRESHOLD:    # use # to ensure msg is sent only once
                self.send_repeat(chat_id, text)

            rds.hset(key, 'users', ','.join(last_users))

        else:
            rds.hset(key, 'text', text.encode('utf-8'))
            rds.hset(key, 'users', username)

    def send_repeat(self, chat_id, text):

        # If '好安静' then send a random xkcd comic
        if text == u'好安静':
            comic = xkcd.getRandomComic()
            log.info('Triggered repeat, sending comic(id=%s) to %s'
                     % (comic.number, chat_id))
            text = '{}: {}\n{}'.format(comic.number, comic.getTitle(), comic.getImageLink())
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='xkcd', url=comic.link),
                    InlineKeyboardButton(text='explain', url=comic.getExplanation()),
                ]
            ])
            self.bot.sendMessage(chat_id=chat_id, text=text, reply_markup=keyboard)

        else:

            log.info('Triggered repeat, sending msg to %s' % chat_id)
            self.bot.sendMessage(chat_id=chat_id, text=text)

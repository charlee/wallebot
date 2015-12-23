import re
import random
from hanziconv import HanziConv
from .base import CommandHandler, MessageHandler

TAGS_DISPLAY_MAX = 20
TAGS_KEY = 'tags:%d'

class TagsCommandHandler(CommandHandler):

    aliases = ('tags', 't')

    def handle(self, msg, params):
        from wallebot.app import rds
        key = TAGS_KEY % msg.chat_id
        tags = rds.smembers(key)

        tags = map(lambda x:(x, HanziConv.toSimplified(x.decode('utf-8')).encode('utf-8')), tags)
        params = map(lambda x:HanziConv.toSimplified(x.decode('utf-8')).encode('utf-8'), params)

        positive_params = [ p for p in params if not p.startswith('-') ]
        negative_params = [ p[1:] for p in params if p.startswith('-') ]

        tags = filter(lambda x:all(k in x[1] for k in positive_params), tags)
        tags = filter(lambda x:all(k not in x[1] for k in negative_params), tags)

        if tags:

            more_msg = ''

            if len(tags) > TAGS_DISPLAY_MAX:
                more_msg = "\n...and %d tags more" % (len(tags) - TAGS_DISPLAY_MAX)
                tags = random.sample(tags, TAGS_DISPLAY_MAX)

            tags = map(lambda x:x[0], tags)

            tags = sorted(list(tags))
            text = '\n'.join('#' + tag for tag in tags)

            if more_msg:
                text += more_msg

            self.bot.sendMessage(chat_id=msg.chat_id, text=text)
            

        

class TagsMessageHandler(MessageHandler):


    def test(self, msg):
        return msg.text and (msg.text[0] == '#' or ' #' in msg.text)


    def handle(self, msg):

        from wallebot.app import rds

        text = msg.text.encode('utf-8').replace('\n', ' ').replace(' ', '  ')
        text = ' %s ' % text
        tags = re.findall(r' #.+? ', text)

        if tags:
            tags = map(lambda x:x.strip('# '), tags)
            key = TAGS_KEY % msg.chat_id
            for tag in tags:
                rds.sadd(key, tag)

            print "%s: Added tags: %s" % (msg.chat_id, ', '.join(tags))

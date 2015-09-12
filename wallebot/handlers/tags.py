import re
from .base import CommandHandler, MessageHandler

class TagsCommandHandler(CommandHandler):

    aliases = ('tags', 't')

    __KEY__ = 'tags:%d'

    def handle(self, msg, params):
        from wallebot.app import rds
        key = self.__KEY__ % msg.chat_id
        tags = rds.smembers(key)

        tags = filter(lambda x:all(k in x for k in params), tags)

        if tags:
            tags = sorted(list(tags))
            text = '\n'.join('#' + tag for tag in tags)
            self.bot.sendMessage(chat_id=msg.chat_id, text=text)
            

        

class TagsMessageHandler(MessageHandler):

    __KEY__ = 'tags:%d'

    def test(self, msg):
        return msg.text and (msg.text[0] == '#' or ' #' in msg.text)


    def handle(self, msg):

        from wallebot.app import rds

        text = msg.text.encode('utf-8').replace('\n', ' ').replace(' ', '  ')
        text = ' %s ' % text
        tags = re.findall(r' #.+? ', text)

        if tags:
            tags = map(lambda x:x.strip('# '), tags)
            key = self.__KEY__ % msg.chat_id
            rds.sadd(key, *tags)

            print "%s: Added tags: %s" % (msg.chat_id, ', '.join(tags))

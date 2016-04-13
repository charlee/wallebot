import re
import random
from hanziconv import HanziConv
from wallebot.fulltext_search import FullTextSearch
from .base import CommandHandler, MessageHandler

TAGS_DISPLAY_MAX = 20

class TagsCommandHandler(CommandHandler):

    aliases = ('tags', 't')

    def handle(self, msg, params):

        fts = FullTextSearch(str(msg.chat_id))

        params = ( HanziConv.toSimplified(x.decode('utf-8')) for x in params )
        params = ( 'NOT %s' % x[1:] if x.startswith('-') else x for x in params )

        keyword = ' '.join(params)

        print '%s: Querying keyword %s...' % (msg.chat_id, keyword)

        (total, tags) = fts.search(keyword, limit=None)

        if tags:

            more_msg = ''

            if len(tags) > TAGS_DISPLAY_MAX:
                more_msg = "\n...and %d tags more" % (len(tags) - TAGS_DISPLAY_MAX)
                tags = random.sample(tags, TAGS_DISPLAY_MAX)

            text = '\n'.join('#' + tag for tag in tags)

            if more_msg:
                text += more_msg

            self.bot.sendMessage(chat_id=msg.chat_id, text=text)
            

class TagsMessageHandler(MessageHandler):

    def test(self, msg):
        return msg.text and (msg.text[0] == '#' or ' #' in msg.text)


    def handle(self, msg):

        fts = FullTextSearch(str(msg.chat_id))

        text = msg.text.replace('\n', ' ').replace(' ', '  ')
        text = ' %s ' % text
        tags = re.findall(r' #.+? ', text)

        if tags:
            tags = map(lambda x:x.strip('# '), tags)
            fts.add_documents(tags)

            print "%s: Added tags: %s" % (msg.chat_id, ', '.join(tags))

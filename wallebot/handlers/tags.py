import re
import random
import opencc
from wallebot.fulltext_search import FullTextSearch
from .base import CommandHandler, MessageHandler

TAGS_DISPLAY_MAX = 20

class TagsCommandHandler(CommandHandler):

    aliases = ('tags', 't')

    def handle(self, msg, params):

        chat_id = msg['chat']['id']

        fts = FullTextSearch(str(chat_id))

        params = ( opencc.convert(x.decode('utf-8')) for x in params )
        params = ( 'NOT %s' % x[1:] if x.startswith('-') else x for x in params )

        keyword = ' '.join(params)

        print '%s: Querying keyword %s...' % (chat_id, keyword)

        (total, tags) = fts.search(keyword, limit=None)

        if tags:

            more_msg = ''

            if len(tags) > TAGS_DISPLAY_MAX:
                more_msg = "\n...and %d tags more" % (len(tags) - TAGS_DISPLAY_MAX)
                tags = random.sample(tags, TAGS_DISPLAY_MAX)

            text = '\n'.join('#' + tag for tag in tags)

            if more_msg:
                text += more_msg

            self.bot.sendMessage(chat_id=chat_id, text=text)
            

class TagsMessageHandler(MessageHandler):

    def test(self, msg):
        text = msg['text']
        return text and (text.startswith('#') or ' #' in text)


    def handle(self, msg):

        chat_id = msg['chat']['id']
        fts = FullTextSearch(str(chat_id))

        text = msg['text'].replace('\n', ' ').replace(' ', '  ')
        text = ' %s ' % text
        tags = re.findall(r' #.+? ', text)

        if tags:
            tags = map(lambda x:x.strip('# '), tags)
            for tag in tags:
                (total, results) = fts.search(tag, limit=1)
                if total == 0:
                    fts.add_document(tag)
                    print "%s: Added tag: %s" % (chat_id, tag)

            print "%s: Added tags: %s" % (chat_id, ', '.join(tags))

import re
import random
import logging
from wallebot.fulltext_search import FullTextSearch
from . import Handler
from telepot.namedtuple import InlineQueryResultArticle
from wallebot.hzconvert import convert

log = logging.getLogger(__name__)

TAGS_DISPLAY_MAX = 20

# binds user to specific group. key => value: user_id => group_id

class TagsHandler(Handler):
    '''Provides tags related features.

    This handler will catch all the tags (starts with `#`) and store them in full text
    search engine. Use `/t` command to find matched tags and display them randomly.

    Commands:
        /t <query>  Query for existing tags. (alias: `/tags <query>`)

                    The following operators can be used.

                    - AND, <space>: and
                    - OR: or
                    - `-`: not
    '''

    USER_GROUP_BINDING_KEY = 'tags:user_group_binding:%s'
    aliases = ['tags', 't']

    def command(self, msg, params):
        '''Command handler. Implements `/t` command.'''

        chat_id = msg['chat']['id']

        fts = FullTextSearch(str(chat_id))

        params = (convert(x) for x in params)
        params = ('NOT %s' % x[1:] if x.startswith('-') else x for x in params)

        keyword = ' '.join(params)

        log.info('%s: Querying keyword %s...' % (chat_id, keyword))

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

    def query(self, query_id, query_string, from_id):

        from wallebot.app import rds

        binding_key = self.USER_GROUP_BINDING_KEY % from_id
        chat_id = rds.get(binding_key)

        fts = FullTextSearch(str(chat_id))

        params = query_string.split(' ')
        params = (convert(x) for x in params)
        params = ('NOT %s' % x[1:] if x.startswith('-') else x for x in params)

        keyword = ' '.join(params)
        log.info('%s: Inline querying keyword %s...' % (chat_id, keyword))

        (total, tags) = fts.search(keyword, limit=TAGS_DISPLAY_MAX)

        results = []
        if tags:
            for tag in tags:
                t = '#{}'.format(tag)
                results.append(InlineQueryResultArticle(
                    id=t,
                    title=t,
                    input_message_content=dict(message_text=t)
                ))

        return results

    def get_result(self, result_id):
        return result_id

    def message(self, msg):
        '''Message handler. Store all the tags to full text search engine.'''

        from wallebot.app import rds

        text = msg['text']
        if not text and (text.startswith('#') or ' #' in text):
            return

        chat_id = msg['chat']['id']
        user_id = msg['from']['id']

        # bind user to latest chat group for the inline bot
        binding_key = self.USER_GROUP_BINDING_KEY % user_id
        rds.set(binding_key, chat_id)

        fts = FullTextSearch(str(chat_id))

        text = msg['text'].replace('\n', ' ').replace(' ', '  ')
        text = ' %s ' % text
        tags = re.findall(r' #.+? ', text)

        if tags:
            tags = map(lambda x: x.strip('# '), tags)
            for tag in tags:
                (total, results) = fts.search(tag, limit=1)
                if total == 0:
                    fts.add_document(tag)
                    print "%s: Added tag: %s" % (chat_id, tag)

            print "%s: Added tags: %s" % (chat_id, ', '.join(tags))

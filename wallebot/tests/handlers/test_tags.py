from mock import Mock, patch
from wallebot.handlers.tags import TagsHandler
from wallebot.tests.base import WallEBaseTestCase

# return value of full text search engine
tags = ['TEXT1', 'TEXT2', 'TEXT3', 'TEXT4', 'TEXT5',
        'TEXT6', 'TEXT7', 'TEXT8', 'TEXT9', 'TEXT10']

fts_return_value = (len(tags), tags)


@patch('wallebot.handlers.tags.FullTextSearch')
class TagsHandlerTestCase(WallEBaseTestCase):

    TEST_TAGS_DISPLAY_MAX = 5

    def setUp(self):
        super(TagsHandlerTestCase, self).setUp()
        self.bot = Mock()
        self.handler = TagsHandler(self.bot)
        self.handler.TAGS_DISPLAY_MAX = self.TEST_TAGS_DISPLAY_MAX

    def make_command(self, params):
        return self.make_group_text('/t {}'.format(' '.join(params)))

    def test_command(self, mock_fts):
        '''Test if /t command can show tags randomly.'''

        mock_fts.return_value.search.return_value = fts_return_value

        params = ['TAG']
        msg = self.make_command(params)

        self.handler.command(msg, params)

        # inspect the API call to telegram
        args = self.bot.method_calls[0][2]
        self.assertEqual(args['chat_id'], msg['chat']['id'])

        tags = [t.strip() for t in args['text'].split('\n') if t.strip()]
        self.assertEqual(len(tags), self.TEST_TAGS_DISPLAY_MAX + 1)

    def test_command_query(self, mock_fts):
        '''Test if the query can be parsed correctly to query keywords.'''
        mock_search = Mock(return_value=fts_return_value)
        mock_fts.return_value.search = mock_search

        params = ['TAG']
        msg = self.make_command(params)
        self.handler.command(msg, params)
        mock_search.assert_called_with('TAG', limit=None)

        params = '(TAG1 OR TAG2) -TAG3'.split(' ')
        msg = self.make_command(params)
        self.handler.command(msg, params)
        mock_search.assert_called_with('(TAG1 OR TAG2) NOT TAG3', limit=None)

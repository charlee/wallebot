from mock import Mock, ANY

from wallebot.bot import WallEBot
from wallebot.handlers import Handler
from wallebot.tests.base import WallEBaseTestCase


class BotTestCase(WallEBaseTestCase):

    def setUp(self):
        super(BotTestCase, self).setUp()

        self.bot = WallEBot(self.TOKEN)
        self.handler = Mock(Handler, aliases=('tags', 't'))
        self.bot.add_handlers(self.handler)
        self.bot.sendMessage = Mock()

    def test_on_chat_msg_cmd(self):
        '''Test if cmd handler is correctly called on chat cmds.'''
        msg = self.make_group_text('/t TAG')
        self.bot.on_chat_message(msg)
        self.handler.command.assert_called_with(msg, ['TAG'])

        msg = self.make_group_text('/tags TAG1 TAG2')
        self.bot.on_chat_message(msg)
        self.handler.command.assert_called_with(msg, ['TAG1', 'TAG2'])

    def test_on_chat_msg_denial(self):
        '''Test if denial works correctly.'''
        msg = self.make_group_text('/t TAG')
        for _ in range(self.bot.CMD_QUOTA + 1):
            self.bot.on_chat_message(msg)

        self.bot.sendMessage.assert_called_with(chat_id=msg['chat']['id'], text=ANY)

    def test_on_chat_msg_non_text(self):
        '''Test if the on_chat_msg ignores non-text msg.'''
        msg = self.make_group_text('test')
        del msg['text']
        msg['audio'] = 'audio'

        self.bot.on_chat_message(msg)

        self.handler.command.assert_not_called()
        self.handler.message.assert_not_called()

    def test_on_chat_msg_regular_msg(self):
        '''Test if regular messages are handled by message handlers.'''
        msg = self.make_group_text('message')
        self.bot.on_chat_message(msg)
        self.handler.message.assert_called_with(msg)

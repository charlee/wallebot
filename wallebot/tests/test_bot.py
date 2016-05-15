from mock import Mock, ANY

from wallebot.bot import WallEBot
from wallebot.handlers import Handler
from wallebot.tests.base import WallEBaseTestCase


class BotTestCase(WallEBaseTestCase):

    TOKEN = '123456'

    def setUp(self):
        bot = WallEBot(self.TOKEN)
        self.handler = Mock(Handler, aliases=('tags', 't'))

        bot.add_handlers(self.handler)
        bot.sendMessage = Mock()

        self.bot = bot

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

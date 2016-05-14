from mock import MagicMock, Mock, patch

from wallebot.bot import WallEBot
from wallebot.handlers import CommandHandler
from wallebot.tests.base import WallEBaseTestCase


class BotTestCase(WallEBaseTestCase):

    TOKEN = '123456'

    def setUp(self):
        bot = WallEBot(self.TOKEN)
        self.cmd_handler = Mock(CommandHandler, aliases=('tags', 't'))
        self.msg_handler = Mock()
        self.inline_handler = Mock()
        self.cron_handler = Mock()

        bot.add_command(self.cmd_handler)
        bot.add_msg_handler(self.msg_handler)
        bot.add_inline_handler(self.inline_handler)
        bot.add_cron_handler(self.cron_handler)

        self.bot = bot

    def test_on_chat_msg_cmd(self):
        msg = self.make_group_text('/t TAG')
        self.bot.on_chat_message(msg)
        self.cmd_handler.handle.assert_called_with(msg, ['TAG'])

        msg = self.make_group_text('/tags TAG1 TAG2')
        self.bot.on_chat_message(msg)
        self.cmd_handler.handle.assert_called_with(msg, ['TAG1', 'TAG2'])

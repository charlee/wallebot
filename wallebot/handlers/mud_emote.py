import os
import json
from .base import CommandHandler

TAGS_DISPLAY_MAX = 20
TAGS_KEY = 'tags:%d'

class MudEmoteCommandHandler(CommandHandler):

    aliases = ('chat', 'e')
    HELP_CMD_COUNT = 100
    
    def __init__(self, bot):
        super(MudEmoteCommandHandler, self).__init__(bot)

        # load emote.json
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'emote.json')
        self.emotes = json.loads(open(path).read())

    def get_emote(self, action, target_type='none'):
        msg_dict = self.emotes.get(action)
        if not msg_dict:
            return

        msg = None
        if target_type == 'self':
            msg = msg_dict.get('self')

        if msg is None or target_type == 'nobody':
            msg = msg_dict.get('nobody')

        if msg is None or target_type == 'other':
            msg = msg_dict.get('other')

        return msg
            

    def handle(self, msg, params):
        if not params:
            if msg.chat.type == 'private':
                keys = sorted(self.emotes.keys())
                for n in range(0, len(keys), self.HELP_CMD_COUNT):
                    text = ', '.join(keys[n:n+self.HELP_CMD_COUNT])
                    self.bot.sendMessage(chat_id=msg.chat_id, text=text)
            return

        action = params[0].strip()
        target = params[1] if len(params) >= 2 else None

        chat_id = msg['chat']['id']
        username = msg['from']['username']

        # process target before use
        if target:
            if target.startswith('@'):
                target = target[1:]

        if target:
            if target == username:
                emote = self.get_emote(action, 'self')
            else:
                emote = self.get_emote(action, 'other')
        else:
            emote = self.get_emote(action, 'nobody')

        if emote:
            emote = emote.replace('%u', username)
            if target and target != username:
                emote = emote.replace('%t', target)
            
        if emote and '%t' not in emote:
            self.bot.sendMessage(chat_id=chat_id, text=emote)
    

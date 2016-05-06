import redis
import time
from config_loader import load_config
from bot import WallEBot
from handlers.tags import TagsCommandHandler, TagsMessageHandler, TagsInlineHandler
from handlers.repeat import RepeatMessageHandler
from handlers.morse import MorseCodeHandler
from handlers.mud_emote import MudEmoteCommandHandler
from handlers.api import APICommandHandler, APIMessageHandler


cfg = load_config()

rds = redis.StrictRedis(host=cfg.REDIS_HOST, db=cfg.REDIS_DB)
bot = WallEBot(cfg.TELEGRAM_TOKEN)

bot.add_command(TagsCommandHandler(bot))
bot.add_msg_handler(TagsMessageHandler(bot))
bot.add_inline_handler(TagsInlineHandler(bot))

bot.add_msg_handler(RepeatMessageHandler(bot))
bot.add_msg_handler(MorseCodeHandler(bot))
bot.add_command(APICommandHandler(bot))
bot.add_msg_handler(APIMessageHandler(bot))
bot.add_command(MudEmoteCommandHandler(bot))

def run():
    bot.message_loop()
    print('Listening...')

    while True:
        time.sleep(10)

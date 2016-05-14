import redis
import time
from config_loader import load_config
from bot import WallEBot
from handlers.tags import TagsHandler
from handlers.repeat import RepeatHandler
from handlers.morse import MorseCodeHandler
from handlers.mud_emote import MudEmoteHandler


cfg = load_config()

rds = redis.StrictRedis(host=cfg.REDIS_HOST, db=cfg.REDIS_DB)
bot = WallEBot(cfg.TELEGRAM_TOKEN)

bot.add_handlers(TagsHandler, MorseCodeHandler, MudEmoteHandler, RepeatHandler)


def run():
    bot.message_loop()
    print('Listening...')

    while True:
        time.sleep(10)

import redis
from config_loader import load_config
from bot import WallEBot
from handlers.tags import TagsCommandHandler, TagsMessageHandler
from handlers.stats import StatsMessageHandler, StatsCronHandler
from handlers.repeat import RepeatMessageHandler
from handlers.morse import MorseCodeHandler
from handlers.api import APICommandHandler, APIMessageHandler


cfg = load_config()

rds = redis.StrictRedis(host=cfg.REDIS_HOST, db=cfg.REDIS_DB)
bot = WallEBot(cfg.TELEGRAM_TOKEN)

bot.add_command(TagsCommandHandler(bot.bot))
bot.add_msg_handler(TagsMessageHandler(bot.bot))
#bot.add_msg_handler(StatsMessageHandler(bot.bot))
bot.add_msg_handler(RepeatMessageHandler(bot.bot))
#bot.add_cron_handler(StatsCronHandler(bot.bot))
bot.add_msg_handler(MorseCodeHandler(bot.bot))
bot.add_command(APICommandHandler(bot.bot))
bot.add_msg_handler(APIMessageHandler(bot.bot))

def run():
    bot.run()

import pytz
import schedule
from datetime import datetime
from .base import MessageHandler, CronHandler

__RANK_KEY__ = 'stats:%s:%s'        # chat_id, date
__LIST_KEY__ = 'stats:chatlist'

def _get_date():
    from wallebot.app import cfg

    timezone = pytz.timezone(cfg.TIMEZONE)
    now = datetime.now(timezone)
    return now.strftime('%Y%m%d')

    return key
    


class StatsMessageHandler(MessageHandler):

    def test(self, msg):
        return True

    def handle(self, msg):

        from wallebot.app import rds
        today = _get_date()

        username = msg.from_user.username

        list_key = __LIST_KEY__
        rank_key = __RANK_KEY__ % (msg.chat_id, today)

        rds.sadd(list_key, msg.chat_id)
        rds.zincrby(rank_key, username)



class StatsCronHandler(CronHandler):
    
    def schedule(self):
        print "Stats scheduled at every day 23:59"
        schedule.every().day.at("23:59").do(self.handle)

    def handle(self):
        

        from wallebot.app import rds, cfg

        today = _get_date()
        list_key = __LIST_KEY__

        chat_ids = rds.smembers(list_key)

        for chat_id in chat_ids:

            rank_key = __RANK_KEY__ % (chat_id, today)

            ranks = rds.zrangebyscore(rank_key, 1, '+inf', start=0, num=10, withscores=True)
            ranks.append(('test', '10'))        # TODO: remove
            ranks.sort(key=lambda x:x[1], reverse=True)

            text = 'Top 10 @ %s\n*******************\n%s' % (today, '\n'.join('@%s - %d' % (p[0], int(p[1])) for p in ranks))

            self.bot.sendMessage(chat_id=chat_id, text=text)


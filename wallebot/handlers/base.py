import pytz
from dateutil.tz import tzlocal
from datetime import datetime

class CommandHandler(object):

    def __init__(self, bot):
        self.bot = bot


    def handle(self, msg, params):
        raise NotImplemented


class MessageHandler(object):

    def __init__(self, bot):
        self.bot = bot

    def test(self, msg):
        """
        Test if message matches this handler.
        """
        raise NotImplemented


    def handle(self, msg):
        """
        Handle this message
        """
        raise NotImplemented


class CronHandler(object):


    __CRON__ = ''

    def tzfix(self, time):
        from wallebot.app import cfg

        hour, minute = time.split(':')
        tz = pytz.timezone(cfg.TIMEZONE)
        now = datetime.now()
        target_time = datetime(now.year, now.month, now.day, int(hour), int(minute), 0, tzinfo=tz)

        local_tz = tzlocal()
        target_time.replace(tzinfo=local_tz)

        return target_time.strftime('%H:%M')
        

    def __init__(self, bot):
        self.bot = bot
        self.schedule()

    def schedule(self):
        raise NotImplemented

    def handle(self):
        raise NotImplemented

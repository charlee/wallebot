import pytz
from tzlocal import get_localzone
from datetime import datetime

class CommandHandler(object):

    def __init__(self, bot):
        self.bot = bot


    def handle(self, msg, params):
        raise NotImplemented


class InlineHandler(object):
    def __init__(self, bot):
        self.bot = bot

    def query(self, query_id, query_string, from_id):
        raise NotImplemented

    def get_result(self, result_id):
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
        now = datetime.now(tz)
        target_time = datetime(now.year, now.month, now.day, int(hour), int(minute), 0, tzinfo=tz)

        local_tz = get_localzone()
        target_time = target_time.astimezone(local_tz)

        return target_time.strftime('%H:%M')
        

    def __init__(self, bot):
        self.bot = bot
        self.schedule()

    def schedule(self):
        raise NotImplemented

    def handle(self):
        raise NotImplemented

import os

# set this item in env! (WALLEBOT_TELEGRAM_TOKEN)
#TELEGRAM_TOKEN='token'

BASEDIR = os.path.dirname(__file__)

REDIS_HOST = '127.0.0.1'
REDIS_DB = 0


# handler config
TIMEZONE = 'US/Eastern'

FULLTEXT_SEARCH_INDEX_DIR = os.path.join(BASEDIR, 'fulltext_search_index')

DEBUG = True

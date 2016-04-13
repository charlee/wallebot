from wallebot.app import rds
from wallebot.handers.tags import TAGS_KEY
from wallebot.fulltext_search import FullTextSearch

chat_id = str(sys.argv[1])

key = TAGS_KEY % chat_id
tags = rds.smembers(key)

print len(tags)

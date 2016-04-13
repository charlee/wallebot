import sys
from wallebot.app import rds
from wallebot.fulltext_search import FullTextSearch

chat_id = str(sys.argv[1])


TAGS_KEY = 'tags:%s'
key = TAGS_KEY % chat_id
tags = rds.smembers(key)

tags = [ t.decode('utf-8') for t in tags ]

fts = FullTextSearch(chat_id)
fts.add_documents(tags)

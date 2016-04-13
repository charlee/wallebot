import sys
from wallebot.fulltext_search import FullTextSearch

chat_id = str(sys.argv[1])
params = sys.argv[2:]
keyword = ' '.join(params)

keyword = keyword.decode('utf-8')


fts = FullTextSearch(chat_id)
(total, tags) = fts.search(keyword, limit=20)
print "Total: %s" % total
print "\n".join(tags)

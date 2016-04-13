# -*- coding: utf-8 -*-

from wallebot.fulltext_search import FullTextSearch

if __name__ == '__main__':
    f = FullTextSearch()
    #f.add_document(u'羡慕霍师傅赞')
    #f.add_document(u'羡慕陈总')

    results = f.search(u'羡')
    for result in results:
        print result





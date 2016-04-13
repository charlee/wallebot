# -*- coding: utf-8 -*-

import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, NGRAMWORDS
from whoosh.qparser import QueryParser


class FullTextSearch(object):

    def __init__(self, path):

        from wallebot.app import cfg
        schema = Schema(
            ngrams=NGRAMWORDS(minsize=1, maxsize=2),
            content=TEXT(stored=True, phrase=False)
        )

        if not os.path.exists(cfg.FULLTEXT_SEARCH_INDEX_DIR):
            os.mkdir(cfg.FULLTEXT_SEARCH_INDEX_DIR)

        index_path = os.path.join(cfg.FULLTEXT_SEARCH_INDEX_DIR, path)

        if not os.path.exists(index_path):
            os.mkdir(index_path)
            self.ix = create_in(index_path, schema)
        else:
            self.ix = open_dir(index_path)


    def add_document(self, content):
        writer = self.ix.writer()
        writer.add_document(ngrams=content, content=content)
        writer.commit()

    def add_documents(self, contents):
        writer = self.ix.writer()
        for content in contents:
            writer.add_document(ngrams=content, content=content)
        writer.commit()
        
        
    def search(self, keyword, limit=20):
        qp = QueryParser("ngrams", schema=self.ix.schema)
        q = qp.parse(keyword)

        with self.ix.searcher() as searcher:
            hits = searcher.search(q)
            results = (hits.scored_length(), [s['content'] for s in hits])

        return results


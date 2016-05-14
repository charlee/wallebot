# -*- coding: utf-8 -*-


class Handler(object):

    aliases = []

    def __init__(self, bot):
        self.bot = bot

    def command(self, msg, params):
        '''Deal with command.'''
        pass

    def message(self, msg):
        '''Deal with text message.'''
        pass

    def query(self, query_id, query_string, from_id):
        '''Deal with inline query.'''
        pass

    def get_result(self, result_id):
        '''Deal with inline query result selecting.'''
        pass

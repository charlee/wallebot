import unittest

class WallEBaseTestCase(unittest.TestCase):

    TOKEN = '123456'

    def make_text(self, text, type='group'):
        return {
            'from': {
                'username': 'test_user',
                'first_name': 'Test',
                'last_name': 'User',
                'id': 2000001,
            },
            'text': text,
            'chat': {
                'id': 1000001,
                'type': type,
                'title': 'Test Group',
            },
            'date': 1463148210,
            'message_id': 1,
        }

    def make_group_text(self, text):
        return self.make_text(text, type='group')

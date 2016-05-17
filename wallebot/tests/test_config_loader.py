import unittest
from wallebot import config_loader

from mock import patch


class ConfigLoaderTestCase(unittest.TestCase):

    @patch('wallebot.config_loader.os')
    @patch('wallebot.config_loader.config')
    def test_load_config(self, mock_config, mock_os):
        '''Test load_config method.'''

        mock_config.TEST_ITEM1 = 'item1'
        mock_config._BEGIN_WITH_UNDERSCORE = 'underscore'
        mock_config.shall_not_exist = 'shall_not_exist'

        mock_os.environ = {
            'WALLEBOT_ENV1': 'env1',
            'REGULAR_ENV': 'shall_not_exist',
        }

        cfg = config_loader.load_config()

        self.assertEqual(cfg.TEST_ITEM1, 'item1')
        self.assertEqual(cfg._BEGIN_WITH_UNDERSCORE, 'underscore')
        self.assertFalse(hasattr(cfg, 'shall_not_exist'))

        self.assertEqual(cfg.ENV1, 'env1')
        self.assertFalse(hasattr(cfg, 'REGULAR_ENV'))

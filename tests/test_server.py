import unittest

from context import server
from context import exceptions


class TestServer(unittest.TestCase):

    TEST_CONFIG_FILES_PATH = 'tests/data/'
    DEFAULT_CONFIG_RELATIVE_PATH = './prom2teams/config.ini'

    def test_get_config_with_invalid_path(self):
        invalid_relative_path = self.TEST_CONFIG_FILES_PATH + 'invalid_path'

        self.assertRaises(FileNotFoundError,
                          server.get_config,
                          self.DEFAULT_CONFIG_RELATIVE_PATH,
                          invalid_relative_path)

    def test_get_config_without_required_keys_should_raise_exception(self):
        empty_config_relative_path = self.TEST_CONFIG_FILES_PATH + \
                                    'empty_config.ini'

        self.assertRaises(exceptions.MissingConnectorConfigKeyException,
                          server.get_config,
                          self.DEFAULT_CONFIG_RELATIVE_PATH,
                          empty_config_relative_path)

    def test_get_config_without_override(self):
        provided_config_relative_path = self.TEST_CONFIG_FILES_PATH + \
                                        'without_overriding_defaults.ini'
        config = server.get_config(self.DEFAULT_CONFIG_RELATIVE_PATH,
                                   provided_config_relative_path)

        self.assertEqual(config.get('HTTP Server', 'Host'), '0.0.0.0')
        self.assertEqual(config.get('HTTP Server', 'Port'), '8089')
        self.assertTrue(config.get('Microsoft Teams', 'Connector'))

    def test_get_config_overriding_defaults(self):
        provided_config_relative_path = self.TEST_CONFIG_FILES_PATH + \
                                        'overriding_defaults.ini'
        config = server.get_config(self.DEFAULT_CONFIG_RELATIVE_PATH,
                                   provided_config_relative_path)

        self.assertEqual(config.get('HTTP Server', 'Host'), '1.1.1.1')
        self.assertEqual(config.get('HTTP Server', 'Port'), '9089')
        self.assertTrue(config.get('Microsoft Teams', 'Connector'))


if __name__ == '__main__':
    unittest.main()

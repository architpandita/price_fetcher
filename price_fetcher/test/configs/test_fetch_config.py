import unittest
from unittest.mock import patch, mock_open
# Import the class YamlParser
from src.configs.fetch_config import YamlParser


class TestYamlParser(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="key: value")
    @patch("os.path.join", return_value="./src/configs/test_config.yaml")
    @patch("yaml.load", return_value={"key": "value"})
    def test_read_config_default_path(self, mock_yaml_load, mock_path_join, mock_open):
        # Test reading a config with the default path
        result = YamlParser.read_config("test_config.yaml")

        # Assertions
        mock_open.assert_called_once_with("./src/configs/test_config.yaml")
        mock_yaml_load.assert_called_once()
        self.assertEqual(result, {"key": "value"})



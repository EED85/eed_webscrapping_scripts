# import pytest
# from unittest.mock import patch
# import yaml

# # import eed_webscrapping_scripts

# # Mock function to replace load_config
# def mock_get_config():
#     with open('config.yaml', 'r') as file:
#         return yaml.safe_load(file)

# # Fixture to use the mock_load_config function
# @pytest.fixture
# def get_config_test():
#     with patch('eed_webscrapping_scripts.dwd.get_config', side_effect=mock_get_config):
#         yield mock_get_config

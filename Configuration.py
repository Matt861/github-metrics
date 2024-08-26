import os
from jproperties import Properties
from dotenv import load_dotenv
from pathlib import Path

p = Path(__file__).resolve()


class Configuration:
    configs = Properties()
    with open('app-config.properties', 'rb') as config_file:
        configs.load(config_file)

    load_dotenv()

    github_api_key1 = os.getenv('GITHUB_API_KEY1')
    github_api_key2 = os.getenv('GITHUB_API_KEY2')
    github_api_key3 = os.getenv('GITHUB_API_KEY3')
    github_api_key4 = os.getenv('GITHUB_API_KEY4')
    github_api_key5 = os.getenv('GITHUB_API_KEY5')
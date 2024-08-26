import itertools
from Configuration import Configuration


class ApiTokenRotator:
    def __init__(self):
        api_tokens = [Configuration.github_api_key1, Configuration.github_api_key2, Configuration.github_api_key3,
                      Configuration.github_api_key4, Configuration.github_api_key5]
        self.api_tokens = api_tokens
        self.current_token = itertools.cycle(self.api_tokens)

    def get_next_token(self):
        return next(self.current_token)

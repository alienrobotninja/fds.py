from typing import Dict

from ape.api.accounts import AccountAPI


class Mail:
    def __init__(self, config: Dict, account: AccountAPI):
        self.config = config
        self.account = account

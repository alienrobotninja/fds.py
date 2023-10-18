from typing import Dict

from ape.api.accounts import AccountAPI

# from fds.fds_ens2 import FDSENS2
from fds.fds_mail import Mail
from fds.fds_tx import Tx


class User:
    def __init__(self, config: Dict, attrs: Dict, account: AccountAPI):
        if not attrs.get("subdomain"):
            raise ValueError("Subdomain must be defined")
        if not attrs.get("wallet"):
            raise ValueError("Wallet must be defined")
        self.config = config
        self.account = account
        self.Mail = Mail(self.config, self.account)
        self.Tx = Tx(self.config, self.account)

"""
Copyright 2023 The FairDataSociety Authors
This file is part of the FairDataSociety library.

The FairDataSociety library is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The FairDataSociety library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with the FairDataSociety library. If not, see <http:www.gnu.org/licenses/>.

handles crypto
"""

import json
from typing import Dict

from web3 import Account

# from ape.api.accounts import Account
from fds.fds_crypto import Crypto


class WalletClass:
    def __init__(self, attrs: Dict):
        self.address = attrs.get("address") or ""
        self.publicKey = attrs.get("publicKey") or ""
        self.privateKey = attrs.get("privateKey") or ""


class Wallet:
    def __init__(self):
        self.wallet = None
        self.wallet_v3 = None

    def generate(self, password):
        account = Account.create()
        wallet = WalletClass(
            {
                "address": account.address.lower(),
                "publicKey": Crypto.private_to_public_key(account._private_key),
                "privateKey": account._private_key,
            }
        )
        self.wallet = wallet
        self.wallet_v3 = Account.encrypt(account.privateKey, password)
        # * https://stackoverflow.com/questions/43380042/purpose-of-return-self-python
        return self

    def from_json(self, wallet_json, password):
        try:
            account = Account.decrypt(wallet_json, password)
            wallet = WalletClass(
                {
                    "address": account.address.lower(),
                    "publicKey": Crypto.private_to_public_key(account._private_key),
                    "privateKey": account._private_key,
                }
            )
            return wallet
        except ValueError as e:
            if str(e) == "Key derivation failed - possibly wrong passphrase":
                return False
            else:
                raise e

    def encrypt(self, private_key, password):
        try:
            wallet_v3 = Account.encrypt(private_key, password)
            wallet_json = json.dumps(wallet_v3)
            return wallet_json
        except Exception as e:
            raise e

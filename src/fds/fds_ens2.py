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

mailbox smart contracts
"""


from typing import Dict

from ape.api.accounts import AccountAPI

from fds.contracts.ENSRegistry import EnsRegistry

KEY_STRING = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"  # noqa: 501


class FDSENS2:
    def __init__(self, account: AccountAPI, config: Dict):
        self.account = account
        self.config = config

        self.ensRegistry = EnsRegistry(self.account, self.config.get("subdomainRegistrarAddress"))

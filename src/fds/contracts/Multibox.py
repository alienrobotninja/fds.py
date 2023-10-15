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

handles Multibox contract
"""

from typing import Union

from ape import networks, project
from ape.api.accounts import AccountAPI
from ape.api.transactions import ReceiptAPI
from ape.types import AddressType

from fds.utils.Exceptions import AccountNotSetUp


class MultiBox:
    def __init__(self, account: AccountAPI, contract_address: Union[AddressType, None] = None):
        self.account = account
        self.contract_address = contract_address
        self.contract = None
        self.web3 = networks.provider._web3

        if not self.account:
            raise AccountNotSetUp("Set up user account first")

        if contract_address:
            self.contract = project.Multibox.at(self.contract_address)
        else:
            return self.deploy()

    def deploy(self):
        self.contract = project.Multibox.deploy(sender=self.account)
        # * call the createRoot method and initialise the contract
        self.contract.init(sender=self.account)

    def getRoots(self) -> ReceiptAPI:
        return self.contract.getRoots()  # type: ignore

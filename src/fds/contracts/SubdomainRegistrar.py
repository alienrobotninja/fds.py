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

handles SubdomainRegistrar contract
"""
from typing import Union

from ape import networks, project
from ape.api.accounts import AccountAPI
from ape.api.transactions import ReceiptAPI
from ape.types import AddressType


class SubdomainRegistrarContractClass:
    def __init__(self, account: AccountAPI, contract_address: Union[AddressType, None] = None):
        self.account = account
        self.contract_address = contract_address
        self.contract = None
        self.web3 = networks.provider._web3

        if contract_address:
            self.contract = project.SubdomainRegistrar.at(self.contract_address)

    def getRootNode(self) -> str:
        return self.contract.rootNode()  # type: ignore

    def register(self, label: int, owner_address: AddressType) -> ReceiptAPI:
        """
        Register a name that's not currently registered
        @param label The hash of the label to register.
        @param owner The address of the new owner.
        """

        self.label = label.to_bytes(32, byteorder="big")
        self.owner_address = owner_address
        self.label = f"0x{self.label.hex()}"  # type: ignore

        return self.contract.register(self.label, self.owner_address, sender=self.account)  # type: ignore # noqa: 501

    def getExpiryTime(self, label: int):
        self.label = label.to_bytes(32, byteorder="big")
        self.label = f"0x{self.label.hex()}"  # type: ignore

        expiryTime = self.contract.expiryTimes(self.label)  # type: ignore

        return expiryTime

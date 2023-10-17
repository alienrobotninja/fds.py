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

handles EnsRegistry contract
"""

from typing import Union

from ape import networks, project
from ape.api.accounts import AccountAPI
from ape.api.transactions import ReceiptAPI
from ape.types import AddressType


class EnsRegistry:
    def __init__(self, account: AccountAPI, contract_address: Union[AddressType, None] = None):
        self.account = account
        self.contract_address = contract_address
        self.contract = None
        self.web3 = networks.provider._web3

        if contract_address:
            self.contract = project.ENSRegistry.at(self.contract_address)

    # ? interacting with the contract methods
    # * returns the address of the owner
    def owner(self, node: Union[int, str, bytes]) -> str:
        if isinstance(node, int):
            self.node = node.to_bytes(32, byteorder="big")
            self.node = f"0x{node.hex()}"  # type: ignore
        else:
            self.node = node  # type: ignore

        return self.contract.owner(self.node)  # type: ignore

    def setResolver(self, node: Union[int, str, bytes], address: AddressType) -> ReceiptAPI:
        if isinstance(node, int):
            self.node = node.to_bytes(32, byteorder="big")
            self.node = f"0x{node.hex()}"  # type: ignore
        else:
            self.node = node  # type: ignore

        return self.contract.setResolver(self.node, address, sender=self.account)  # type: ignore

    def getResolver(self, node: Union[int, str, bytes]) -> str:
        if isinstance(node, int):
            self.node = node.to_bytes(32, byteorder="big")
            self.node = f"0x{node.hex()}"  # type: ignore
        else:
            self.node = node  # type: ignore

        return self.contract.resolver(self.node)  # type: ignore

    def setOwner(self, node: Union[int, str, bytes], address: AddressType) -> ReceiptAPI:
        if isinstance(node, int):
            self.node = node.to_bytes(32, byteorder="big")
            self.node = f"0x{node.hex()}"  # type: ignore
        else:
            self.node = node  # type: ignore

        return self.contract.setOwner(self.node, address, sender=self.account)  # type: ignore

    # * Returns the TTL of a node, and any records associated with it.
    def getTTL(self, node: Union[int, str, bytes]) -> int:
        if isinstance(node, int):
            self.node = node.to_bytes(32, byteorder="big")
            self.node = f"0x{node.hex()}"  # type: ignore
        else:
            self.node = node  # type: ignore

        return self.contract.ttl(self.node)  # type: ignore

    def setTTL(self, node: Union[int, str, bytes], ttl: int) -> ReceiptAPI:
        if isinstance(node, int):
            self.node = node.to_bytes(32, byteorder="big")
            self.node = f"0x{node.hex()}"  # type: ignore
        else:
            self.node = node  # type: ignore
        self.ttl = ttl
        return self.contract.setTTL(self.node, self.ttl, sender=self.account)  # type: ignore

    # TODO: Add all other methods if required.

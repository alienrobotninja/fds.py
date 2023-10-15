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

handles KeyValueTree contract
"""

from typing import List, Tuple, Union

from ape import networks, project
from ape.api.accounts import AccountAPI
from ape.api.transactions import ReceiptAPI
from ape.types import AddressType

from fds.utils.convert import int_to_bytes32
from fds.utils.Exceptions import AccountNotSetUp


class KeyValueTree:
    def __init__(self, account: AccountAPI, contract_address: Union[AddressType, None] = None):
        self.account = account
        self.contract_address = contract_address
        self.contract = None
        self.web3 = networks.provider._web3

        if not self.account:
            raise AccountNotSetUp("Set up user account first")

        if contract_address:
            self.contract = project.KeyValueTree.at(self.contract_address)

    def getSharedId(self) -> ReceiptAPI:
        return self.contract.getSharedId()  # type: ignore

    def getRootId(self) -> ReceiptAPI:
        return self.contract.getRootId()  # type: ignore

    def setKeyValue(self, nodeId: int, key: int, value: int) -> bool:
        self.nodeId = int_to_bytes32(nodeId)
        self.key = key.to_bytes(32, byteorder="big")
        self.value = value.to_bytes(32, byteorder="big")

        return self.contract.setKeyValue(self.nodeId, self.key, self.value, sender=self.account)  # type: ignore # noqa: 501

    def getKeyValue(self, nodeId: int, key: int) -> ReceiptAPI:
        self.nodeId = int_to_bytes32(nodeId)
        self.key = key.to_bytes(32, byteorder="big")

        return self.contract.getValue(self.nodeId, self.key)  # type: ignore

    def getKeyValues(self, nodeId: int) -> Tuple:
        self.nodeId = int_to_bytes32(nodeId)
        return self.contract.getKeyValues(self.nodeId)  # type: ignore

    def addChildNode(self, parent_node_id: str, sub_node_id: str) -> ReceiptAPI:
        self.parent_node_id = parent_node_id
        self.sub_node_id = sub_node_id

        return self.contract.addChildNode(self.parent_node_id, self.sub_node_id, sender=self.account)  # type: ignore # noqa: 501

    def getChildren(self, parent_node_id: str) -> List:
        self.parent_node_id = parent_node_id

        return self.contract.getChildren(self.parent_node_id)  # type: ignore

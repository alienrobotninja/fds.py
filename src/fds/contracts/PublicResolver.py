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

handles PublicResolver contract
"""
from typing import Tuple, Union

from ape import convert, networks, project
from ape.api.accounts import AccountAPI
from ape.api.transactions import ReceiptAPI
from ape.types import AddressType

from fds.utils.Exceptions import AccountNotSetUp


class PublicResolverClass:
    def __init__(self, account: AccountAPI, contract_address: Union[AddressType, None] = None):
        self.account = account
        self.contract_address = contract_address
        self.contract = None
        self.web3 = networks.provider._web3

        if contract_address:
            self.contract = project.PublicResolver.at(self.contract_address)

    def setAll(
        self,
        node: int,
        address: AddressType,
        content: str,
        multihash: str,
        x: int,
        y: int,
        name: str,
    ) -> ReceiptAPI:
        """
        * Sets all required params in one attempt
        * May only be called by the owner of that node in the ENS registry.
        * @param node The node to update.
        * @param addr The address to set.
        * @param content The content hash to set
        * @param multihash The multihash to set
        * @param x the X coordinate of the curve point for the public key.
        * @param y the Y coordinate of the curve point for the public key.
        * @param name The name to set.
        """

        """
        If x = b'abc' then f"{x}" or "{}".format(x) produces "b'abc'", not "abc".
        If this is desired behavior, use f"{x!r}" or "{!r}".format(x).
        Otherwise, decode the bytes
        """
        self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        self.address = address
        self.content = content.encode("utf-8")
        self.multihash = multihash.encode("utf-8")
        self.x = x.to_bytes(32, byteorder="big")
        self.y = y.to_bytes(32, byteorder="big")
        self.name = name

        return self.contract.setAll(  # type: ignore
            self.node,
            self.address,
            self.content,
            self.multihash,
            self.x,
            self.y,
            self.name,
            sender=self.account,
        )

    def getAll(self, node: int) -> Tuple:
        self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"

        return self.contract.getAll(self.node)  # type: ignore

    def setPublicKey(self, node: int, x: int, y: int) -> ReceiptAPI:
        """
        * Sets the SECP256k1 public key associated with an ENS node.
        * @param node The ENS node to query
        * @param x the X coordinate of the curve point for the public key.
        * @param y the Y coordinate of the curve point for the public key.
        """
        if not self.account:
            raise AccountNotSetUp("Set up user account first")

        self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        self.x = x.to_bytes(32, byteorder="big")
        self.y = y.to_bytes(32, byteorder="big")

        return self.contract.setPubkey(self.node, self.x, self.y, sender=self.account)  # type: ignore # noqa: 501

    def getPublicKey(self, node: int) -> Tuple[int, int]:
        """
        * Returns the SECP256k1 public key associated with an ENS node.
        * Defined in EIP 619.
        * @param node The ENS node to query
        * @return x, y the X and Y coordinates of the curve point for the public key.
        """

        self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"

        return self.contract.pubkey(self.node)  # type: ignore

    def setMultiHash(self, node: int, _hash: str) -> ReceiptAPI:
        """
        * Sets the multihash associated with an ENS node.
        * May only be called by the owner of that node in the ENS registry.
        * @param node The node to update.
        * @param hash The multihash to set.
        """
        if not self.account:
            raise AccountNotSetUp("Set up user account first")

        self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        self.hash = _hash.encode("utf-8")

        return self.contract.setMultihash(self.node, self.hash, sender=self.account)  # type: ignore

    def getMultiHash(self, node: int) -> str:
        """
        * Returns the multihash associated with an ENS node.
        * @param node The ENS node to query.
        * @return The associated multihash.
        """
        self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"

        return convert(self.contract.multihash(self.node), str)  # type: ignore

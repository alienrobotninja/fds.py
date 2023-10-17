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
        node: Union[int, bytes, str],
        address: AddressType,
        content: str,
        multihash: str,
        x: Union[int, str],
        y: Union[int, str],
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
        if not self.account:
            raise AccountNotSetUp("Set up user account first")

        if isinstance(node, int):
            self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        else:
            self.node = node  # type: ignore
        self.address = address
        self.content = content.encode("utf-8")
        self.multihash = multihash.encode("utf-8")
        if isinstance(x, int):
            self.x = x.to_bytes(32, byteorder="big")
        else:
            self.x = x  # type: ignore
        if isinstance(y, int):
            self.y = y.to_bytes(32, byteorder="big")
        else:
            self.y = y  # type: ignore
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

    def getAll(
        self,
        node: Union[int, bytes, str],
    ) -> Tuple:
        if isinstance(node, int):
            self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        else:
            self.node = node  # type: ignore
        return self.contract.getAll(self.node)  # type: ignore

    def setPublicKey(
        self,
        node: Union[int, bytes, str],
        x: Union[int, str],
        y: Union[int, str],
    ) -> ReceiptAPI:
        """
        * Sets the SECP256k1 public key associated with an ENS node.
        * @param node The ENS node to query
        * @param x the X coordinate of the curve point for the public key.
        * @param y the Y coordinate of the curve point for the public key.
        """
        if not self.account:
            raise AccountNotSetUp("Set up user account first")
        if isinstance(node, int):
            self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        else:
            self.node = node  # type: ignore
        if isinstance(x, int):
            self.x = x.to_bytes(32, byteorder="big")
        else:
            self.x = x  # type: ignore
        if isinstance(y, int):
            self.y = y.to_bytes(32, byteorder="big")
        else:
            self.y = y  # type: ignore

        return self.contract.setPubkey(self.node, self.x, self.y, sender=self.account)  # type: ignore # noqa: 501

    def getPublicKey(
        self,
        node: Union[int, bytes, str],
    ) -> Tuple[bytes, bytes]:
        """
        * Returns the SECP256k1 public key associated with an ENS node.
        * Defined in EIP 619.
        * @param node The ENS node to query
        * @return x, y the X and Y coordinates of the curve point for the public key.
        """

        if isinstance(node, int):
            self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        else:
            self.node = node  # type: ignore

        return self.contract.pubkey(self.node)  # type: ignore

    def setMultiHash(self, node: Union[int, bytes, str], _hash: str) -> ReceiptAPI:
        """
        * Sets the multihash associated with an ENS node.
        * May only be called by the owner of that node in the ENS registry.
        * @param node The node to update.
        * @param hash The multihash to set.
        """
        if not self.account:
            raise AccountNotSetUp("Set up user account first")

        if isinstance(node, int):
            self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        else:
            self.node = node  # type: ignore
        self.hash = f"0x{_hash.encode().hex()}"

        return self.contract.setMultihash(self.node, self.hash, sender=self.account)  # type: ignore

    def getMultiHash(
        self,
        node: Union[int, bytes, str],
    ) -> str:
        """
        * Returns the multihash associated with an ENS node.
        * @param node The ENS node to query.
        * @return The associated multihash.
        """
        if isinstance(node, int):
            self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        else:
            self.node = node  # type: ignore

        return bytes.fromhex(convert(self.contract.multihash(self.node).hex(), str)[2:]).decode("utf-8")  # type: ignore # noqa: 501

    def setAddr(self, node: Union[int, bytes, str], address: AddressType) -> ReceiptAPI:
        if isinstance(node, int):
            self.node = f"0x{node.to_bytes(32, byteorder='big').hex()}"
        else:
            self.node = node  # type: ignore

        return self.contract.setAddr(self.node, address)  # type: ignore

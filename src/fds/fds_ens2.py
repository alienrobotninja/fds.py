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


from typing import Dict, Tuple, Union

from ape import convert, networks
from ape.api.accounts import AccountAPI
from ape.api.transactions import ReceiptAPI
from eth_utils import keccak

from fds.contracts.ENSRegistry import EnsRegistry
from fds.contracts.PublicResolver import PublicResolverClass
from fds.contracts.SubdomainRegistrar import SubdomainRegistrarContractClass
from fds.utils.convert import getNameHash, getPublicKey

KEY_STRING = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"  # noqa: 501


class FDSENS2:
    def __init__(self, account: AccountAPI, config: Dict):
        self.account = account
        self.config = config
        self.web3 = networks.provider._web3

        self.ensRegistry = EnsRegistry(self.account, self.config.get("ensRegistryContract"))
        self.SubdomainRegistrar = SubdomainRegistrarContractClass(
            self.account, self.config.get("subdomainRegistrarAddress")
        )
        self.PublicResolver = PublicResolverClass(
            self.account, self.config.get("publicResolverAddress")
        )

    def registerSubdomain(self, sub_domain: str) -> ReceiptAPI:
        self.hash = keccak(sub_domain.encode())
        return self.SubdomainRegistrar.register(self.hash, self.account.address)

    def setResolver(self, sub_domain: str) -> ReceiptAPI:
        self.node = getNameHash(sub_domain, self.config.get("domain"))
        self.address = self.config.get("publicResolverAddress")

        return self.ensRegistry.setResolver(self.node, self.address)  # type: ignore

    def setAll(self, sub_domain: str, content: str, multihash: str, name: str) -> ReceiptAPI:
        self.node = getNameHash(sub_domain, self.config.get("domain"))

        self.content = content
        self.multihash = multihash
        self.publicKey = getPublicKey(self.account)
        self.publicKeyX = self.publicKey[:66]
        self.publicKeyY = "0x" + self.publicKey[66:130]
        self.name = name

        return self.PublicResolver.setAll(
            self.node,
            self.account.address,
            self.content,
            self.multihash,
            self.publicKeyX,
            self.publicKeyY,
            self.name,
        )

    def getAll(self, sub_domain: str) -> Tuple:
        self.node = getNameHash(sub_domain, self.config.get("domain"))

        return self.PublicResolver.getAll(self.node)

    def setAddr(self, sub_domain: str) -> ReceiptAPI:
        self.node = getNameHash(sub_domain, self.config.get("domain"))

        return self.PublicResolver.setAddr(self.node, self.account.address)

    def setPubKey(self, sub_domain: str) -> ReceiptAPI:
        self.node = getNameHash(sub_domain, self.config.get("domain"))
        self.publicKey = getPublicKey(self.account)
        self.publicKeyX = self.publicKey[:66]
        self.publicKeyY = "0x" + self.publicKey[66:130]

        return self.PublicResolver.setPublicKey(self.node, self.publicKeyX, self.publicKeyY)

    def setMultiHash(self, sub_domain: str, multihash: str) -> ReceiptAPI:
        self.node = getNameHash(sub_domain, self.config.get("domain"))

        return self.PublicResolver.setMultiHash(sub_domain, multihash)

    def getMultiHash(self, sub_domain: str) -> str:
        self.node = getNameHash(sub_domain, self.config.get("domain"))

        return self.PublicResolver.getMultiHash(sub_domain)

    def getOwner(self, sub_domain: str) -> str:
        self.node = getNameHash(sub_domain, self.config.get("domain"))

        return self.ensRegistry.owner(self.node)

    def getPubKey(self, sub_domain: str) -> Union[str, bool]:
        """
        * Get public key of subdoman
        * @param {string} subdomain name
        * @returns {string | boolean} returns false if invalid
        """
        self.node = getNameHash(sub_domain, self.config.get("domain"))

        return self.getPubKeyRaw(self.node)

    def getPubKeyRaw(self, node: str) -> Union[str, bool]:
        """
        * Get public key of subdoman
        * @param {string} subdomain name
        * @returns {string | boolean} returns false if invalid
        */
        """
        self.keyCoordsX, self.keyCoordsY = self.PublicResolver.getPublicKey(node)
        self.keyCoordsX = convert(self.keyCoordsX, str)
        self.keyCoordsY = convert(self.keyCoordsY, str)

        self.keyStr = "04" + str(self.keyCoordsX[2:66]) + str(self.keyCoordsY[2:66])

        if self.keyStr != KEY_STRING:
            return self.keyStr
        else:
            return False

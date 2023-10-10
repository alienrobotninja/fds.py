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

    handles Contract interactions
"""

from pathlib import Path
# from ape.managers.chain import instance_at
from typing import Dict, List, Optional, Union

import ape
# * ape imports
from ape import Contract, project
from ape.api.accounts import AccountAPI
from ape.contracts.base import ContractContainer, ContractInstance, ContractTransactionHandler
from ape.types import AddressType
from ape.utils import BaseInterfaceModel
from ethpm_types import ABI, ContractType

from fds.utils.Exceptions import AccountNotFoundException, NotImplementedException

# class FDSContract(AccountAPI):
#     """
#     FDSContract class
#         constructor:
#             account: account to sign and send transactions
#             abi: abi of the contract. can be of type list, ABI, Dictionary or file containing the abi in json format
#             bytecode: hex format
#     """

#     account: AccountAPI = None
#     raw_address: AddressType

#     def __init__(
#         self,
#         account: AccountAPI = None,
#     ):
#         super().__init__()
#         self.account = account

#     @property
#     def contract(
#         self, address: AddressType, abi: Optional[Union[List[ABI], Dict, str, Path]] = None
#     ) -> ContractInstance:
#         """
#         to use the methods of the Contract class of ape.
#         i.e. to use something like contract = Contract("0xdead") which will make a contract container to work with
#         """
#         self.address = address
#         self.abi = abi
#         if self.abi:
#             return self.chain_manager.contracts.instance_at(self.address, abi=self.abi)

#         return self.chain_manager.contracts.instance_at(self.address)

#     def Contract(self, address: AddressType) -> ContractInstance:
#         self.address = address

#         return self.contract(self.address)

#     def at(self, address: AddressType, abi: Optional[Union[List[ABI], Dict, str, Path]] = None):
#         self.address = address
#         self.abi = abi

#         return self.contract(self.address, self.abi)

#     def deploy(
#         self, contract: ContractContainer, *args, publish: bool = False, **kwargs
#     ) -> ContractInstance:
#         if not self.account:
#             raise AccountNotFoundException("Account hash not been set up yet.")

#         return super().deploy(contract, *args, publish, **kwargs)

#     # * For ape AccountAPI class
#     @property
#     def address(self) -> AddressType:
#         self.raw_address  # TODO: implement this

#     def sign_message(self):
#         raise NotImplementedException()

#     def sign_transaction(self):
#         raise NotImplementedException()


class FDSContract:
    def __init__(
        self,
        account: AccountAPI = None,
    ):
        # super().__init__()
        self.account = account

    def at(
        self, address: AddressType, abi: Optional[Union[List[ABI], Dict, str, Path]] = None
    ) -> ContractInstance:
        if not self.account:
            raise AccountNotFoundException("Account has not been set yet")
            return
        self.address = address
        self.abi = abi
        return Contract(address=self.address, abi=self.abi)

    def deploy(
        self, contract: ContractContainer, *args, publish: bool = False, **kwargs
    ) -> ContractInstance:
        if not self.account:
            raise AccountNotFoundException("Account hash not been set up yet.")
            return

        return super().deploy(contract, *args, publish, **kwargs)

    def deploy_from_abi(
        self,
        address: AddressType,
        abi: Optional[Union[List[ABI], Dict, str, Path]] = None,
        **kwargs,
    ) -> ContractContainer:
        if not self.account:
            raise AccountNotFoundException("Account has not been set yet")
            return
        self.address = address
        self.abi = abi
        self.contract = Contract(address=self.address, abi=self.abi)

        return self.account.deploy(self.contract, **kwargs)

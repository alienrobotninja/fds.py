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

        return self.account.deploy(contract, *args, publish, **kwargs)

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

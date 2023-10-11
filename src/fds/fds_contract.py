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


# from ape.managers.chain import instance_at

# * ape imports
# import ape
from ape import Contract  # , project
from ape.api.accounts import AccountAPI
from ape.api.transactions import ReceiptAPI, TransactionAPI
from ape.contracts.base import ContractContainer, ContractInstance
from ape.types import AddressType

# * Fds modules
from fds.utils.Exceptions import AccountNotFoundException, ContractNotFoundException
from fds.utils.types import AbiType

# from ape.utils import BaseInterfaceModel
# from ethpm_types import ABI  , ContractType

# from pandas import DataFrame


class FDSContract:
    def __init__(self, account: AccountAPI):
        self.account = account
        self.contract_address = None

    def at(self, address: AddressType, abi: AbiType = None) -> ContractInstance:
        if not self.account:
            raise AccountNotFoundException("Account has not been set yet.")

        self.contract_address = address  # type: ignore
        self.abi = abi
        self.contract = Contract(address=self.contract_address, abi=self.abi)  # type: ignore
        return self.contract

    def deploy(
        self, contract: ContractContainer, *args, publish: bool = False, **kwargs
    ) -> ContractInstance:
        if not self.account:
            raise AccountNotFoundException("Account has not been set up yet.")

        self.contract = self.account.deploy(contract, *args, publish=publish, **kwargs)
        self.contract_address = self.contract.address  # type: ignore
        return self.contract

    def call(
        self,
        txn: TransactionAPI,
        send_everything: bool = False,
        private: bool = False,
        **signer_options,
    ) -> ReceiptAPI:
        """
        Make a transaction call.
        """

        if not self.contract_address or not self.contract_address == "0x":
            raise ContractNotFoundException("Contract is not deployed yet.")
        if not self.account:
            raise AccountNotFoundException("Account has not been set up yet.")

        return self.account.call(
            txn=txn, send_everything=send_everything, private=private, **signer_options
        )

    # TODO: Decide whether we need this as ape has already a built in query method to get events
    # def getPastEvents(
    #     self,
    #     *columns: List[str],
    #     event_name: str,
    #     start_block: int = 0,
    #     stop_block: Optional[int] = None,
    #     step: int = 1,
    #     engine_to_use: Optional[str] = None,
    # ) -> DataFrame:
    #     # self.contract = contract
    #     # print(self.contract, self.contract_address, self.contract_address)
    #     # if not self.contract or not self.contract_address == "0x" or not self.contract_address:
    #     #     raise ContractNotFoundException("Contract is not deployed yet.")

    #     self.events = getattr(self.contract, event_name).query(
    #         *columns,
    #         start_block=start_block,
    #         stop_block=stop_block,
    #         step_block=step,
    #         engine_to_use=engine_to_use,
    #     )

    #     return self.events

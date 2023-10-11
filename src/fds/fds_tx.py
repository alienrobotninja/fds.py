from ape.api.accounts import AccountAPI
from ape.contracts.base import ContractContainer, ContractInstance
from ape.types import AddressType

from fds.fds_contract import FDSContract
from fds.utils.types import AbiType


class Tx:
    def __init__(self, account: AccountAPI):
        self.account = account
        self.contract_address = None

    def getContract(
        self, account: AccountAPI, address: AddressType, abi: AbiType
    ) -> ContractInstance:
        self.account = account
        self.address = address
        self.abi = abi

        contract = FDSContract(self.account)
        return contract.at(address=address, abi=self.abi)

    def deployContract(
        self, contract: ContractContainer, *args, publish: bool = False, **kwargs
    ) -> ContractInstance:
        contract = FDSContract(self.account)  # type: ignore

        return contract.deploy(contract=contract, *args, publish=publish, **kwargs)

    def syncNonce(self, account: AccountAPI) -> int:
        """
        Sync the nonce with the account. This is used to prevent
        accidental re - authenticating a user when they change their account.

        @param account - The account to sync the nonce with. Must be an instance of AccountAPI.

        @return The nonce
        """
        self.account = account

        return self.account.nonce

from typing import Optional, Tuple, Union

from ape import chain, networks
from ape.api.accounts import AccountAPI
from ape.api.transactions import ReceiptAPI
from ape.contracts.base import ContractContainer, ContractInstance
from ape.types import AddressType, MessageSignature
from eth_account import Account
from eth_account.messages import encode_defunct

# * fds libraries
from fds.fds_contract import FDSContract
from fds.utils.Exceptions import InaccessibleGatewayException
from fds.utils.types import VRS, AbiType


class Tx:
    def __init__(self, account: AccountAPI):
        self.account = account
        self.contract_address = None

    def getContract(self, address: AddressType, abi: AbiType) -> ContractInstance:
        # self.account = account
        self.address = address
        self.abi = abi

        contract = FDSContract(self.account)
        return contract.at(address=address, abi=self.abi)

    def deployContract(
        self, contract: ContractContainer, *args, publish: bool = False, **kwargs
    ) -> ContractInstance:
        fdscontract = FDSContract(self.account)  # type: ignore

        return fdscontract.deploy(contract=contract, *args, publish=publish, **kwargs)

    def syncNonce(self) -> int:
        """
        Sync the nonce with the account. This is used to prevent
        accidental re - authenticating a user when they change their account.

        @param account - The account to sync the nonce with. Must be an instance of AccountAPI.

        @return The nonce
        """
        # self.account = account

        return self.account.nonce

    def pay(
        self, to_address: AddressType, amount: Union[str, int, None] = None, gas: int = 6000000
    ) -> ReceiptAPI:
        """
        https://docs.apeworx.io/ape/stable/userguides/transactions.html
        Another way to use a static-fee transaction (without having to
        provide gas_price) is to set the key-value argument type equal to 0x00.
        When declaring type="0x0" and not specifying a gas_price, the gas_price
        gets set using the provider's estimation.
        """

        self.web3 = networks.provider._web3
        # self.account = account
        self.to_address = to_address
        self.gas = gas

        # * convert the value to int using ape's converter
        if not isinstance(amount, int):
            amount = chain.conversion_manager.convert(amount, int)

        # Estimate the gas required for the transaction
        required_gas_price = self.web3.eth.estimate_gas(
            {
                "to": self.to_address,
                "from": self.account.address,
                "value": amount,
            }
        )

        # Calculate the actual gas price
        actual_gas_price = self.web3.eth.gas_price * required_gas_price
        if self.gas < actual_gas_price:
            self.gas = actual_gas_price

        # Calculate the value to be sent subtracting the gas
        value = int(amount) - self.gas  # type: ignore

        tx_params = {
            "to": self.to_address,
            "from": self.account.address,
            # * letting ape to set the best gas price
            # "gas": self.web3.eth.gas_price,
            # "gasPrice": self.gas,
            "value": value,
            "data": "",
        }

        txn = networks.ecosystem.create_transaction(**tx_params)  # type: ignore

        receipt = self.account.call(txn)

        return receipt

    def getBalace(self, address: AddressType) -> int:
        self.web3 = networks.provider._web3

        try:
            return self.web3.eth.get_balance(address)
        except Exception as e:
            raise InaccessibleGatewayException("Can't access gateway", e)

    def getBlockNumber(self):
        """
        Returns the latest block number of the ecosystem
        """
        return networks.provider.get_block("latest")

    def sign(
        self, account: AddressType, message: str, key: Optional[str] = None
    ) -> MessageSignature:
        """
        https://eth-account.readthedocs.io/en/stable/eth_account.html#eth_account.account.Account.sign_message
        """
        self.account = account  # type: ignore
        self.key = key
        message_hash = encode_defunct(text=message)
        if key:
            signed_message = self.account.sign_message(message_hash, key)  # type: ignore
            return signed_message.signature  # type: ignore

        signed_message = self.account.sign_message(message_hash)  # type: ignore
        return signed_message.signature  # type: ignore

    def recover(
        self, message: str, signature: str, vrs: Optional[Tuple[VRS, VRS, VRS]] = None
    ) -> AddressType:
        """
        https://eth-account.readthedocs.io/en/stable/eth_account.html#eth_account.account.Account.recover_message
        """
        message_hash = encode_defunct(text=message)
        if vrs:
            signer = Account.recover_message(message_hash, vrs=vrs)
            return signer

        signer = Account.recover_message(message_hash, signature=signature)
        return signer

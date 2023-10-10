- `fds_contract.py`

```py
class FDSContract(AccountAPI):
    """
    FDSContract class
        constructor:
            account: account to sign and send transactions
            abi: abi of the contract. can be of type list, ABI, Dictionary or file containing the abi in json format
            bytecode: hex format
    """

    account: AccountAPI = None
    raw_address: AddressType

    def __init__(
        self,
        account: AccountAPI = None,
    ):
        super().__init__()
        self.account = account

    @property
    def contract(
        self, address: AddressType, abi: Optional[Union[List[ABI], Dict, str, Path]] = None
    ) -> ContractInstance:
        """
        to use the methods of the Contract class of ape.
        i.e. to use something like contract = Contract("0xdead") which will make a contract container to work with
        """
        self.address = address
        self.abi = abi
        if self.abi:
            return self.chain_manager.contracts.instance_at(self.address, abi=self.abi)

        return self.chain_manager.contracts.instance_at(self.address)

    def Contract(self, address: AddressType) -> ContractInstance:
        self.address = address

        return self.contract(self.address)

    def at(self, address: AddressType, abi: Optional[Union[List[ABI], Dict, str, Path]] = None):
        self.address = address
        self.abi = abi

        return self.contract(self.address, self.abi)

    def deploy(
        self, contract: ContractContainer, *args, publish: bool = False, **kwargs
    ) -> ContractInstance:
        if not self.account:
            raise AccountNotFoundException("Account hash not been set up yet.")

        return super().deploy(contract, *args, publish, **kwargs)

    # * For ape AccountAPI class
    @property
    def address(self) -> AddressType:
        self.raw_address  # TODO: implement this

    def sign_message(self):
        raise NotImplementedException()

    def sign_transaction(self):
        raise NotImplementedException()
```

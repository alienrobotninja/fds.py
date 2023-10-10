import pytest
from ape import accounts

from fds.fds_contract import FDSContract


@pytest.mark.use_network("ethereum:local:test")
def test_load_contract_from_abi(owner, address):
    abi = [
        {
            "inputs": [],
            "name": "getCount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "increment",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]

    # address = "0x13370Df4d8fE698f2c186A18903f27e00a097331"  # random address
    fdscontract = FDSContract(owner)
    loaded_contract = fdscontract.at(address=address, abi=abi)

    assert loaded_contract.address == address

    # * test contract method
    assert loaded_contract.getCount() == 0

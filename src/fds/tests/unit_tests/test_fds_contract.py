from ape import accounts

from fds.fds_contract import FDSContract


def test_load_contract_from_abi(owner):
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

    account = owner
    address = account.address
    fdscontract = FDSContract(owner)
    loaded_contract = fdscontract.at(address=address, abi=abi)

    print(dir(loaded_contract))
    print(type(loaded_contract))

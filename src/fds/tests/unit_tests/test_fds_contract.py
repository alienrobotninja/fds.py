# from ape import accounts, networks
from ape import networks  # , project

from fds.fds_contract import FDSContract

# from pandas import DataFrame


def test_load_contract_at(owner, solidity_contract_instance, ABI):
    # address = "0x13370Df4d8fE698f2c186A18903f27e00a097331"  # random address
    address = solidity_contract_instance.address
    fdscontract = FDSContract(owner)
    loaded_contract = fdscontract.at(address=address, abi=ABI)

    assert loaded_contract.address == address
    assert loaded_contract.balance == 0
    assert loaded_contract.owner() == owner

    # * test contract method
    assert loaded_contract.getCount() == 0
    loaded_contract.increment(sender=owner)
    assert loaded_contract.count() == 1


def test_deploy_contract(owner, fdsContractDeploy):
    # fdscontract = FDSContract(owner)
    # contract = fdscontract.deploy(project.SolidityTestContract)
    contract = fdsContractDeploy
    assert contract.address == "0xF2Df0b975c0C9eFa2f8CA0491C2d1685104d2488"
    assert contract.balance == 0
    assert contract.owner() == owner

    # * test contract method
    assert contract.getCount() == 0
    contract.increment(sender=owner)
    assert contract.count() == 1


def test_call(sender, eth_tester_provider):
    # contract = fdsContractDeploy

    txn = networks.ecosystem.create_transaction(value="1 wei", data="")

    txn = sender.prepare_transaction(txn)

    call = sender.call(txn)

    assert txn.gas_limit == eth_tester_provider.max_gas, "Test setup failed - gas limit unexpected."

    assert call.data.hex() == "0x"
    assert call.value == 1


# def test_getPastEvents(sender):
#     fdscontract = FDSContract(sender)
#     contract = fdscontract.deploy(project.SolidityTestContract)

#     events = fdscontract.getPastEvents("*", event_name="getCount", start_block=-1)

#     assert isinstance(events, DataFrame)

#     print(events)

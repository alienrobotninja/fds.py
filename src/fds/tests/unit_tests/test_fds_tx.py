from fds.fds_tx import Tx


def test_get_contract(sender, owner, solidity_contract_instance, ABI):
    contract_address = solidity_contract_instance.address

    tx_object = Tx(owner)
    deployed_contract = tx_object.getContract(contract_address, ABI)

    assert deployed_contract.address == contract_address
    assert deployed_contract.balance == 0
    assert deployed_contract.owner() == owner

    # * test contract method
    assert deployed_contract.getCount() == 0
    deployed_contract.increment(sender=sender)
    assert deployed_contract.count() == 1


def test_deploy_contract(owner, solidity_contract_container):
    tx_object = Tx(owner)
    contract = tx_object.deployContract(solidity_contract_container)

    assert contract.balance == 0
    assert contract.owner() == owner

    # * test contract method
    assert contract.getCount() == 0
    contract.increment(sender=owner)
    assert contract.count() == 1


def test_syncNonce(sender, receiver):
    tx_object = Tx(sender)

    nonce = tx_object.syncNonce()

    assert isinstance(nonce, int)

    assert nonce == 0

    # if it's possible send some tx to increase eth balance
    # print(sender.balance)
    sender.transfer(receiver, "10 ether")

    assert tx_object.syncNonce() > 0


def test_pay(sender, receiver):
    tx_object = Tx(sender)

    receipt = tx_object.pay(
        to_address=receiver.address,
        amount="0.1 ether",
    )

    assert receipt
    assert receipt.data.hex() == "0x"
    # assert receipt.to == receiver.address
    assert receipt.gas_used > 0

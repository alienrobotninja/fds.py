import binascii

from ape import networks

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

    assert nonce == 2

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


def test_getBalance(owner):
    tx_object = Tx(owner)
    tx_object.getBalance(owner.address)

    assert tx_object


def test_getBlockNumber(owner):
    tx_object = Tx(owner)

    block_number = tx_object.getBlockNumber()

    assert block_number == networks.provider.get_block("latest")


def test_sign(sender):
    tx_object = Tx(sender)
    text = "I♥FDS"
    signature = tx_object.sign(message=text)

    assert signature
    assert (
        "0x" + binascii.hexlify(signature.encode_vrs()).decode("utf-8")
        == "0x1b2a32f4d3114d78b7793d9c69f049b2eecc592b4038866a0bed7cc6fb248dcb3e3a173f3296298aab6628d68ee1b2fb4194c8731af9f4f1575234e9fccbef13d7"  # noqa: E501
    )

    assert signature.v == 27
    assert (
        "0x" + binascii.hexlify(signature.r).decode("utf-8")
        == "0x2a32f4d3114d78b7793d9c69f049b2eecc592b4038866a0bed7cc6fb248dcb3e"
    )
    assert (
        "0x" + binascii.hexlify(signature.s).decode("utf-8")
        == "0x3a173f3296298aab6628d68ee1b2fb4194c8731af9f4f1575234e9fccbef13d7"
    )


def test_recover(receiver):
    tx_object = Tx(receiver)

    text = "I♥SF"

    vrs = (
        28,
        "0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb3",
        "0x3e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce",
    )

    signer = tx_object.recover(text, vrs=vrs)

    assert signer == "0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E"

    signature = "0xe6ca9bba58c88611fad66a6ce8f996908195593807c4b38bd528d2cff09d4eb33e5bfbbf4d3e39b1a2fd816a7680c19ebebaf3a141b239934ad43cb33fcec8ce1c"  # noqa: E501

    # * test with signature
    signer = tx_object.recover(text, signature=signature)

    assert signer == "0x5ce9454909639D2D17A3F753ce7d93fa0b9aB12E"

    # add checks for other formats like showin here
    # https://eth-account.readthedocs.io/en/stable/eth_account.html#eth_account.account.Account.sign_message

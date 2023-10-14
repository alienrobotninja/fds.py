import pytest
from ape import convert
from ape.exceptions import ContractLogicError

from fds.contracts.PublicResolver import PublicResolverClass


def test_set_all(owner, sender, publicResolverContract, ENS):
    assert ENS.owner(0) == owner.address

    pubResClass = PublicResolverClass(owner, publicResolverContract.address)

    pubResClass.setAll(0, sender.address, "hahaha", "eeehahaha", 16, 17, "jadu")

    addr, content, multihash, x, y, name = pubResClass.getAll(0)

    assert addr == sender.address
    assert content.decode().replace("\x00", "") == "hahaha"
    assert multihash.decode().replace("\x00", "") == "eeehahaha"
    assert convert(x, int) == 16
    assert convert(y, int) == 17
    assert name.replace("\x00", "") == "jadu"


def test_set_publickey(owner, publicResolverContract):
    pubResClass = PublicResolverClass(owner, publicResolverContract.address)
    node = 0
    pubResClass.setPublicKey(node, 22, 34)

    x, y = pubResClass.getPublicKey(node)

    assert convert(x, int) == 22
    assert convert(y, int) == 34


# TODO: fixt this test
def test_multihash(owner, publicResolverContract):
    pubResClass = PublicResolverClass(owner, publicResolverContract.address)
    node = 0
    _hash = "fairDataProtocl"
    pubResClass.setMultiHash(node, _hash)

    returned_hash = pubResClass.getMultiHash(node)

    assert returned_hash == _hash


def test_fail_set_publickey(owner, publicResolverContract):
    pubResClass = PublicResolverClass(owner, publicResolverContract.address)
    node = 1

    with pytest.raises(ContractLogicError):
        # * trying to access other node
        pubResClass.setPublicKey(node, 22, 34)

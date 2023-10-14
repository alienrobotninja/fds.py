import pytest
from ape.exceptions import ContractLogicError

from fds.contracts.ENSRegistry import EnsRegistry


def test_load_ensContract(owner, ENS):
    assert ENS.owner(0) == owner.address


def test_set_resolver(owner, ENS):
    ENS.setResolver(0, owner.address)

    assert ENS.getResolver(0) == owner.address


def test_fail_setting_resolver(owner, ENS):
    with pytest.raises(ContractLogicError):
        ENS.setResolver(1, owner.address)


def test_set_owner(ENS, receiver):
    ENS.setOwner(0, receiver.address)

    assert ENS.owner(0) == receiver.address


def test_fail_setting_owner(owner, ensContract, receiver):
    contract = ensContract

    ENS = EnsRegistry(receiver, contract.address)

    with pytest.raises(ContractLogicError):
        ENS.setOwner(0, owner.address)


def test_set_n_get_ttl(ENS):
    assert ENS.getTTL(0) == 0

    ENS.setTTL(0, 420)

    assert ENS.getTTL(0) == 420


def test_fail_setting_ttl(owner, ensContract):
    contract = ensContract

    ENS = EnsRegistry(owner, contract.address)

    with pytest.raises(ContractLogicError):
        ENS.setTTL(12, 1111)

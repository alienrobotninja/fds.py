import pytest
from ape.exceptions import ContractLogicError

from fds.contracts.SubdomainRegistrar import SubdomainRegistrarContractClass


def test_load_ens_contract(owner, subDomainRegistrarContract):
    contract = subDomainRegistrarContract
    src = SubdomainRegistrarContractClass(owner, contract.address)
    node = 1
    node = node.to_bytes(32, byteorder="big")
    assert src.getRootNode() == node


def test_register(owner, ensContract):
    src = SubdomainRegistrarContractClass(owner, ensContract.address)

    # ENS.setOwner(0, owner.address)
    with pytest.raises(ContractLogicError):
        src.register(0, owner.address)

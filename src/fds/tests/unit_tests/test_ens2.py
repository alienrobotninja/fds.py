from fds.fds_ens2 import FDSENS2

# from ape.api.transactions import ReceiptAPI

# import pytest
# from ape.exceptions import ContractLogicError
# TODO


def test_setup_ens2Class(owner, ensContract, subDomainRegistrarContract, publicResolverContract):
    config = {
        "domain": "fds.eth",
        "ensRegistryContract": ensContract.address,
        "subdomainRegistrarAddress": subDomainRegistrarContract.address,
        "publicResolverAddress": publicResolverContract.address,
    }
    ens2 = FDSENS2(owner, config)

    assert ens2.config.get("ensRegistryContract") == ensContract.address


# def test_registerSubdomain(ens2Class):
#     sub_domain = "0"

#     receipt = ens2Class.registerSubdomain(sub_domain)

#     # print(receipt)

#     assert receipt


# def test_setResolver(ens2Class):
#     sub_domain = "0x0000000000000000000000000000000000000000000000000000000000000000"
#     receipt = ens2Class.setResolver(sub_domain)

#     assert isinstance(receipt, ReceiptAPI)

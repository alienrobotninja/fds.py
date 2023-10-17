from pathlib import Path

import ape  # type: ignore
import pytest
from ape import project
from ape.contracts.base import ContractContainer, ContractInstance
from ethpm_types import ContractType

from fds.contracts.ENSRegistry import EnsRegistry
from fds.contracts.KeyValueTree import KeyValueTree
from fds.fds_contract import FDSContract
from fds.fds_crypto import Crypto
from fds.fds_ens2 import FDSENS2
from fds.fds_wallet import Wallet

# from fds.utils.convert import getNameHash

TEST_CONTRACT_ADDRESS = "0x13370Df4d8fE698f2c186A18903f27e00a097331"
PROJECT_PATH = Path(__file__).parent
CONTRACTS_FOLDER = PROJECT_PATH / "data" / "contracts" / "abi"


abi = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "inputs": [],
        "name": "count",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
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
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]


@pytest.fixture(scope="session")
def address():
    return TEST_CONTRACT_ADDRESS


@pytest.fixture(autouse=True)
def crypto_instance():
    return Crypto()


@pytest.fixture(autouse=True)
def test_wallet():
    return Wallet()


@pytest.fixture(autouse=True)
def wallet_instance(test_wallet):
    password = "test_password"
    test_wallet.generate(password)
    return test_wallet


# * Ape fixtures
@pytest.fixture(autouse=True)
def eth_tester_provider(ethereum):
    if not ape.networks.active_provider or ape.networks.provider.name != "test":
        with ethereum.local.use_provider("test") as provider:
            yield provider
    else:
        yield ape.networks.provider


@pytest.fixture(autouse=True)
def setenviron(monkeypatch):
    """
    Sets the APE_TESTING environment variable during tests.

    With this variable set fault handling and IPython command history logging
    will be disabled in the ape console.
    """
    monkeypatch.setenv("APE_TESTING", "1")


@pytest.fixture(scope="session")
def config():
    return ape.config


@pytest.fixture(scope="session")
def convert(chain):
    return chain.conversion_manager.convert


@pytest.fixture(scope="session")
def plugin_manager():
    return ape.networks.plugin_manager


@pytest.fixture(scope="session")
def accounts():
    return ape.accounts


@pytest.fixture(scope="session")
def compilers():
    return ape.compilers


@pytest.fixture(scope="session")
def networks():
    return ape.networks


@pytest.fixture(scope="session")
def chain():
    return ape.chain


@pytest.fixture(scope="session")
def test_accounts(accounts):
    return accounts.test_accounts


@pytest.fixture
def vitalik(accounts):
    return accounts["0xab5801a7d398351b8be11c439e05c5b3259aec9b"]


@pytest.fixture(scope="session")
def owner(test_accounts):
    return test_accounts[0]


@pytest.fixture(scope="session")
def sender(test_accounts):
    return test_accounts[1]


@pytest.fixture(scope="session")
def receiver(test_accounts):
    return test_accounts[2]


@pytest.fixture(scope="session")
def not_owner(test_accounts):
    return test_accounts[3]


@pytest.fixture(scope="session")
def helper(test_accounts):
    return test_accounts[4]


@pytest.fixture
def signer(test_accounts):
    return test_accounts[5]


@pytest.fixture
def geth_account(test_accounts):
    return test_accounts[6]


@pytest.fixture
def geth_second_account(test_accounts):
    return test_accounts[7]


@pytest.fixture
def ethereum(networks):
    return networks.ethereum


@pytest.fixture
def mock_provider(mock_web3, eth_tester_provider):
    web3 = eth_tester_provider.web3
    eth_tester_provider._web3 = mock_web3
    yield eth_tester_provider
    eth_tester_provider._web3 = web3


@pytest.fixture(scope="session")
def get_contract_type():
    def fn(name: str) -> ContractType:
        return ContractType.parse_file(CONTRACTS_FOLDER / f"{name}.json")

    return fn


@pytest.fixture(scope="session")
def solidity_contract_type(get_contract_type) -> ContractType:
    return get_contract_type("SolidityTestContract")


@pytest.fixture(scope="session")
def solidity_contract_container(solidity_contract_type) -> ContractContainer:
    return ContractContainer(contract_type=solidity_contract_type)


@pytest.fixture
def networks_connected_to_tester(eth_tester_provider):
    return eth_tester_provider.network_manager


@pytest.fixture
def solidity_contract_instance(
    owner, solidity_contract_container, networks_connected_to_tester
) -> ContractInstance:
    return owner.deploy(solidity_contract_container)


@pytest.fixture
def ABI():
    return abi


@pytest.fixture
def fdsContractDeploy(owner):
    fdscontract = FDSContract(owner)
    contract = fdscontract.deploy(ape.project.SolidityTestContract)

    return contract


@pytest.fixture
def ensContract(owner):
    return project.ENSRegistry.deploy(sender=owner)


@pytest.fixture
def ENS(owner, ensContract):
    return EnsRegistry(owner, ensContract.address)


@pytest.fixture
def subDomainRegistrarContract(owner, ensContract):
    node = 1
    node = node.to_bytes(32, byteorder="big")
    return project.SubdomainRegistrar.deploy(ensContract.address, node, sender=owner)


@pytest.fixture
def publicResolverContract(owner, ensContract):
    return project.PublicResolver.deploy(ensContract.address, sender=owner)


@pytest.fixture
def multibox(owner):
    mb = project.Multibox.deploy(sender=owner)
    mb.init(sender=owner)

    return mb


@pytest.fixture
def key_value_tree(owner):
    return project.KeyValueTree.deploy(owner.address, sender=owner)


@pytest.fixture
def kvt(owner, key_value_tree):
    return KeyValueTree(owner, key_value_tree.address)


@pytest.fixture
def ens2Class(owner):
    ensContract = project.ENSRegistry.deploy(sender=owner)

    sub_domain = "0x0000000000000000000000000000000000000000000000000000000000000000"
    # label = "0x0fe8b52446c828faa96a2aedf4552d9c63e5fafdad4cb525d5e65c6d713811fd"
    # node = getNameHash(sub_domain, label)

    ensContract.setSubnodeOwner(
        "0x0000000000000000000000000000000000000000000000000000000000000000",
        "0x0fe8b52446c828faa96a2aedf4552d9c63e5fafdad4cb525d5e65c6d713811fd",
        owner,
        sender=owner,
    )

    subDomainRegistrarContract = project.SubdomainRegistrar.deploy(
        ensContract.address, sub_domain, sender=owner
    )
    publicResolverContract = project.PublicResolver.deploy(ensContract.address, sender=owner)

    # print(subDomainRegistrarContract.rootNode().hex())
    # print(ensContract.owner(subDomainRegistrarContract.rootNode()))
    config = {
        "domain": "test.fds.eth",
        "ensRegistryContract": ensContract.address,
        "subdomainRegistrarAddress": subDomainRegistrarContract.address,
        "publicResolverAddress": publicResolverContract.address,
    }
    ens2 = FDSENS2(owner, config)

    return ens2

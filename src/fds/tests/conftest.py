import ape
import pytest

from fds.fds_wallet import Wallet


@pytest.fixture(autouse=True)
def test_wallet():
    return Wallet()


@pytest.fixture(autouse=True)
def wallet_instance(test_wallet):
    password = "test_password"
    test_wallet.generate(password)
    return test_wallet


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


@pytest.fixture(scope="session")
def networks():
    return ape.networks


@pytest.fixture
def ethereum(networks):
    return networks.ethereum


@pytest.fixture(autouse=True)
def eth_tester_provider(ethereum):
    if not ape.networks.active_provider or ape.networks.provider.name != "test":
        with ethereum.local.use_provider("test") as provider:
            yield provider
    else:
        yield ape.networks.provider


@pytest.fixture
def mock_provider(mock_web3, eth_tester_provider):
    web3 = eth_tester_provider.web3
    eth_tester_provider._web3 = mock_web3
    yield eth_tester_provider
    eth_tester_provider._web3 = web3

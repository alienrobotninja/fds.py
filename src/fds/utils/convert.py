# from ape import networks
from typing import Any, Optional

from ape.api.accounts import AccountAPI
from eth_account import Account
from eth_keys import keys
from namehash import namehash  # type: ignore

# web3 = networks.provider._web3


def int_to_bytes32(input: int) -> str:
    return f"0x{input.to_bytes(32, byteorder='big').hex()}"


def getPublicKey(account: AccountAPI, password: str = "a") -> str:
    key_file = account.keyfile
    # Decrypt the private key
    private_key = Account.decrypt(key_file, password)

    pk = keys.PrivateKey(private_key)
    public_key = pk.public_key

    return public_key


def getNameHash(sub_domain: str, domain: Optional[Any]) -> str:
    # return web3.ens.namehash(f"{sub_domain}.{domain}")
    return "0x" + namehash(f"{sub_domain}.{domain}").hex()

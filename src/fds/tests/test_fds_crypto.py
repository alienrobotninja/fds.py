import pytest
from eth_utils import keccak

from fds.fds_crypto import Crypto
from fds.fds_wallet import Wallet


def test_public_key_derivation():
    address1 = "0xecedad96c545979b7e57be4cabeb679ef85c25e2"
    public_key1 = "0x37f91e6ec022b55c08eca29f89e47f6f03ad1af35d3a7b2cacd1514c0c9e31c0358a181b3d50552440a9b1c7ea2942b94b178179a16798bcd7fc77b1cccff309"
    private_key1 = "0x7cbb15a540c3954792bf3729f9b26c0242e745890332bcf2ffeaece345f9d141"

    address2 = "0x74ff5f6a11c3d9782191dc3f3042708e396cbf3c"
    public_key2 = "0xa621164c25da8bb0d87652c0c24d946dc4793f45609fd6006e23e6255646bb32d60af2800b1492aa8d8927c6904f2acab727637c072dbce786a5cd36f18cff86"
    private_key2 = "0x95e8f771761c8cd8a711ca57434ad3769e9fc6fe451561820781efc8ed999a85"

    # * as the last 40 characters or 20 bytes will be the address
    generated_address1 = keccak(hexstr=public_key1).hex()[-40:]

    assert f"0x{generated_address1}" == address1

    generated_address2 = keccak(hexstr=public_key2).hex()[-40:]

    assert f"0x{generated_address2}" == address2

    crypto = Crypto()
    generated_public_key1 = crypto.private_to_public_key(private_key1)
    generated_public_key2 = crypto.private_to_public_key(private_key2)

    assert generated_public_key1 == public_key1
    assert generated_public_key2 == public_key2


def test_calculate_shared_secret():
    crypto = Crypto()

    private_key1 = "0x7cbb15a540c3954792bf3729f9b26c0242e745890332bcf2ffeaece345f9d141"
    recipient_public_key1 = "0x37f91e6ec022b55c08eca29f89e47f6f03ad1af35d3a7b2cacd1514c0c9e31c0358a181b3d50552440a9b1c7ea2942b94b178179a16798bcd7fc77b1cccff309"

    shared_secret = crypto.calculate_shared_secret(private_key1, recipient_public_key1)

    # Assert that the shared_secret is not empty (it should be a bytes-like object)
    assert shared_secret


# def test_encrypt_and_decrypt_string():
#     crypto = Crypto()
#     string_to_encrypt = "Hello, World!"
#     password = b"supersecretpass"  # Should be bytes
#     iv = crypto.generate_random_iv()

#     encrypted_string = crypto.encrypt_string(string_to_encrypt, password, iv)
#     decrypted_string = crypto.decrypt_string(encrypted_string, password, iv)

#     # Assert that the decrypted string matches the original string
#     assert decrypted_string == string_to_encrypt

if __name__ == "__main__":
    test_calculate_shared_secret()

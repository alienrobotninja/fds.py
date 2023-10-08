import json

from fds.fds_wallet import Wallet


def test_generate_wallet(wallet_instance):
    # test_wallet = Wallet()
    # password = "test_password"
    # generated_wallet = test_wallet.generate(password)
    generated_wallet = wallet_instance
    # print(generated_wallet.wallet_v3)

    assert generated_wallet.wallet.address != ""
    assert generated_wallet.wallet.publicKey != ""
    assert generated_wallet.wallet.privateKey != ""
    # * i.e. generated_wallet.wallet_v3 is not None
    assert generated_wallet.wallet_v3


def test_from_json_valid(test_wallet):
    password = "test_password"
    generated_wallet = test_wallet.generate(password)
    wallet_json = json.dumps(generated_wallet.wallet_v3)

    wallet_from_json = test_wallet.from_json(wallet_json, password)

    assert wallet_from_json.address == generated_wallet.wallet.address
    assert wallet_from_json.publicKey == generated_wallet.wallet.publicKey
    assert wallet_from_json.privateKey == generated_wallet.wallet.privateKey


def test_fail_from_json_invalid(test_wallet):
    password = "test_password"
    generated_wallet = test_wallet.generate(password)
    wallet_json = json.dumps(generated_wallet.wallet_v3)

    # Provide an incorrect password to test decryption failure
    invalid_password = "wrong_password"
    try:
        wallet_from_json = test_wallet.from_json(wallet_json, invalid_password)
    except ValueError as e:
        assert str(e) == "MAC mismatch", f"Unexpected error message: {e}"
        return

    # If no exception was raised, the test fails
    assert (
        False
    ), 'Expected a ValueError with message "MAC mismatch", but no exception was raised'


def test_encrypt(test_wallet):
    private_key = "0x7cbb15a540c3954792bf3729f9b26c0242e745890332bcf2ffeaece345f9d141"  # Replace with a valid private key
    password = "test_password"

    wallet_json = test_wallet.encrypt(private_key, password)

    # print(wallet_json)

    assert isinstance(wallet_json, str)

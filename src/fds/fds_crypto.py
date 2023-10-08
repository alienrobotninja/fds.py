"""
Copyright 2023 The FairDataSociety Authors
This file is part of the FairDataSociety library.

The FairDataSociety library is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The FairDataSociety library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with the FairDataSociety library. If not, see <http:www.gnu.org/licenses/>.

handles crypto
"""
import codecs
import hashlib
from binascii import hexlify, unhexlify
from os import urandom

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from eth_keys import keys
from eth_utils import decode_hex


class Crypto:
    @staticmethod
    def generate_random_iv():
        return urandom(16)

    @staticmethod
    def private_to_public_key(private_key):
        # * if in str then process it directly
        if isinstance(private_key, str):
           private_key_hex = private_key
        # * if in bytes then convert it to hex
        elif isinstance(private_key, bytes): 
            private_key_hex = private_key.hex()
        else:
            raise TypeError("Invalid private key format. Expected str or bytes.")
            
        private_key_bytes = decode_hex(private_key_hex)

        if len(private_key_bytes) != 32:
            raise ValueError("Invalid private key length. Expected 64 characters.")

        #private_key_bytes = codecs.decode(private_key, "hex_codec")

        pk = keys.PrivateKey(private_key_bytes)
        return pk.public_key.to_hex()

    @staticmethod
    def calculate_shared_secret(private_key_hex, recipient_public_key_hex):
        # Remove '0x' prefix and convert hex to bytes
        private_key_bytes = unhexlify(private_key_hex[2:])
        recipient_public_key_bytes = unhexlify(recipient_public_key_hex[2:])

        # Make sure the private key is 32 bytes (256 bits) long
        if len(private_key_bytes) != 32:
            raise ValueError("Private key must be a 32 byte hex string")

        # Make sure the public key is 64 bytes (512 bits) long
        if len(recipient_public_key_bytes) != 64:
            raise ValueError("Public key must be a 64 byte hex string")

        # Load the private key
        private_key = ec.derive_private_key(
            int.from_bytes(private_key_bytes, byteorder="big"),
            ec.SECP256K1(),
            default_backend(),
        )

        # Load the recipient's public key
        recipient_public_key = ec.EllipticCurvePublicNumbers(
            int.from_bytes(recipient_public_key_bytes[:32], byteorder="big"),
            int.from_bytes(recipient_public_key_bytes[32:], byteorder="big"),
            ec.SECP256K1(),
        ).public_key(default_backend())

        # Calculate the shared secret
        shared_secret = private_key.exchange(ec.ECDH(), recipient_public_key)

        # Return the shared secret as a hex string
        return shared_secret.hex()

    @staticmethod
    def encrypt_string(string, password, iv):
        # Convert hex to bytes
        # iv = unhexlify(iv)
        string = string.encode("utf-8")
        # Hash the password to create a 32-byte key
        key = hashlib.sha256(password).digest()

        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(string) + encryptor.finalize()

        # Return the encrypted string as a hex string
        return hexlify(encrypted).decode("utf-8")

    @staticmethod
    def decrypt_string(encrypted_hex, password, iv):
        # Convert hex to bytes

        # iv = unhexlify(iv)
        encrypted = unhexlify(encrypted_hex)
        # Hash the password to create a 32-byte key
        key = hashlib.sha256(password).digest()

        cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        # Return the decrypted string as a utf-8 string
        return decrypted.decode("utf-8")
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
from os import urandom

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from eth_keys import keys


class Crypto:
    @staticmethod
    def generate_random_iv():
        return urandom(16)

    @staticmethod
    def private_to_public_key(private_key):
        # Remove "0x" prefix if present
        private_key = private_key.replace("0x", "")

        if len(private_key) != 64:
            raise ValueError("Invalid private key length. Expected 64 characters.")

        private_key_bytes = codecs.decode(private_key, "hex_codec")

        pk = keys.PrivateKey(private_key_bytes)
        return pk.public_key.to_hex()

    @staticmethod
    def calculate_shared_secret(private_key, recipient_public_key):
        # Remove "0x" prefix if present
        private_key = bytes.fromhex(private_key.replace("0x", ""))
        recipient_public_key = bytes.fromhex(recipient_public_key.replace("0x", ""))
        # print(recipient_public_key)

        recipient_public_key = serialization.load_pem_public_key(
            recipient_public_key, backend=default_backend()
        )
        print(recipient_public_key)
        shared_key = private_key.exchange(ec.ECDH(), recipient_public_key)
        return shared_key

    @staticmethod
    def encrypt_string(string, password, iv):
        cipher = Cipher(
            algorithms.AES(password), modes.CTR(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()
        return encryptor.update(string.encode("utf-8")) + encryptor.finalize()

    @staticmethod
    def decrypt_string(string, password, iv):
        cipher = Cipher(
            algorithms.AES(password), modes.CTR(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()
        return (decryptor.update(string) + decryptor.finalize()).decode("utf-8")

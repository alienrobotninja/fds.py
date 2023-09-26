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
from os import urandom

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Crypto:
    def generate_random_iv(self):
        return urandom(16)

    def private_to_public_key(self, private_key):
        private_key = serialization.load_pem_private_key(
            private_key, password=None, backend=default_backend()
        )
        public_key = private_key.public_key()
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def calculate_shared_secret(self, private_key, recipient_public_key):
        recipient_public_key = serialization.load_pem_public_key(
            recipient_public_key, backend=default_backend()
        )
        shared_key = private_key.exchange(ec.ECDH(), recipient_public_key)
        return shared_key

    def encrypt_string(self, string, password, iv):
        cipher = Cipher(
            algorithms.AES(password), modes.CTR(iv), backend=default_backend()
        )
        encryptor = cipher.encryptor()
        return encryptor.update(string.encode("utf-8")) + encryptor.finalize()

    def decrypt_string(self, string, password, iv):
        cipher = Cipher(
            algorithms.AES(password), modes.CTR(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()
        return (decryptor.update(string) + decryptor.finalize()).decode("utf-8")

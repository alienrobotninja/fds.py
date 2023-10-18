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

store files using swarm
"""
# import os
import time
# from binascii import unhexlify
from typing import Dict, List, Union

import requests
from ape.api.accounts import AccountAPI

from fds.fds_crypto import Crypto
from fds.utils.Bee import Bee

# from Crypto.Cipher import AES
# from Crypto.Util.Padding import unpad


POSTAGE_STAMP = "0000000000000000000000000000000000000000000000000000000000000000"  # noqa: 501


class Hash:
    def __init__(self, address, file, time, iv, meta, account):
        self.address = address
        self.file = file
        self.time = time
        self.iv = iv
        self.meta = meta
        self.account = account


# TODO: implement the full thing
class Swarm:
    def __call__(self, config: Dict, account: AccountAPI):
        self.config = config
        self.account = account
        self.gateway = config.get("beeGateway")
        self.rawGateway = self.gateway + "/bytes"  # type: ignore
        self.bee = Bee(self.gateway)  # type: ignore
        self.crypto = Crypto()

    def getSwarmDigest(self, string: str) -> Union[str, None]:
        if string == "/shared/mail":
            return "0x723beeeb4a880dc9432fdf3b1b53df942c4ec162ffda83037f2ad2ef94b22c23"
        elif string == "/shared":
            return "0x23e642b7242469a5e3184a6566020c815689149967703a98c0affc14b9ca9b28"
        elif string == "/":
            "0xc7f5bbf5fe95923f0691c94f666ac3dfed12456cd33bd018e7620c3d93edd5a6"
        else:
            try:
                digest = self.bee.uploadData(POSTAGE_STAMP, string)
            except Exception as e:
                raise (e)

            return "0x" + digest
        return None

    def getSwarmDigestValue(self, swarm_hash: str) -> str:
        self.swarm_hash = swarm_hash.replace("0x", "")
        if self.swarm_hash == "/shared/mail":
            return "0x723beeeb4a880dc9432fdf3b1b53df942c4ec162ffda83037f2ad2ef94b22c23"
        elif self.swarm_hash == "/shared":
            return "0x23e642b7242469a5e3184a6566020c815689149967703a98c0affc14b9ca9b28"
        elif self.swarm_hash == "/":
            "0xc7f5bbf5fe95923f0691c94f666ac3dfed12456cd33bd018e7620c3d93edd5a6"
        else:
            try:
                self.value = self.bee.downloadData(self.swarm_hash)
            except Exception as e:
                raise (e)
        return self.value

    def storeFilesUnencrypted(self, files: List, pin: bool = True) -> str:
        """
        * Store unencrypted file to swarm
        * @param {any} file to store
        * @param {any} encryptedProgressCallback callback
        * @param {any} uploadedProgressCallback callback
        * @param {any} progressMessageCallback callback
        * @returns {Hash} with address, file, time and iv
        """
        self.file = files[0]

        self.metadata = {"name": self.file.name, "type": self.file.type, "size": self.file.size}

        return self.bee.uploadFiles(
            POSTAGE_STAMP, self.file, {"indexDocument": self.metadata.get("name")}
        )

    def storeEncryptedFile(self, file, secret: str, pin: bool = True, metadata: Dict = {}) -> Hash:
        """
        * Store encrypted file to swarm
        * @param {any} file to store
        * @param {any} secret to use
        * @param {any} encryptedProgressCallback callback
        * @param {any} uploadedProgressCallback callback
        * @param {any} progressMessageCallback callback
        * @returns {Hash} with address, file, time and iv
        """
        if metadata is None:
            self.metadata = {}

        self.iv = self.crypto.generate_random_iv()
        self.buffer = self.crypto.encrypt_buffer(file, secret, self.iv)

        self.metadata = {"name": file.name, "type": file.type, "size": file.size, **metadata}

        self.reference = self.bee.uploadFiles(POSTAGE_STAMP, self.buffer, self.metadata["name"])

        return Hash(
            address=self.reference,
            file=file,
            time=int(time.time() * 1000),  # Convert to milliseconds
            iv="0x" + self.iv.hex(),
            meta=self.metadata,
            account=self.account,
        )

    def getDataFromManifest(self, swarm_hash: str) -> Union[str, None]:
        """
        * Get manifest from url
        * @param {any} swarmHash hash
        * @param {any} filename file at hash
        * @returns {any} result of request (manifest)
        """
        self.url = f"{self.gateway}/bzz/{swarm_hash}"
        self.response = requests.get(self.url)
        if self.response.status_code == 200:
            return self.response.content.decode("utf-8")
        else:
            return None

    # def getDecryptedFile(
    #     self, hash: List, secret: str, selected_mailbox: str, selected_wallet: str
    # ):
    #     """
    #     * Get decrypted file
    #     * @param {any} hash location
    #     * @param {any} secret to decrypt
    #     * @param {any} selectedMailbox mailbox to use
    #     * @param {any} selectedWallet wallet to use
    #     * @returns {any} decrypted file
    #     """
    #     self.retrieved_file = self.getDataFromManifest(hash["address"], hash["file"]["name"])

    #     # Decrypt the file
    #     self.cipher = AES.new(unhexlify(secret[2:]), AES.MODE_CTR, iv=unhexlify(hash["iv"][2:34]))
    #     self.decrypted_buffer = unpad(self.cipher.decrypt(self.retrieved_file), AES.block_size)

    #     # Write the decrypted file to disk
    #     self.file_path = os.path.join(selected_mailbox, selected_wallet, hash["name"])
    #     with open(self.file_path, "wb") as f:
    #         f.write(self.decrypted_buffer)

    #     return self.file_path

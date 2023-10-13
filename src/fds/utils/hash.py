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

handles hashes
"""

import os

import requests


# TODO:
class Hash:
    def __init__(self, attrs, account):
        if "address" not in attrs:
            raise ValueError("address must be defined")
        if "file" not in attrs:
            raise ValueError("file must be defined")
        if "time" not in attrs:
            raise ValueError("time must be defined")

        self.address = attrs["address"]
        self.file = attrs["file"]
        self.time = attrs["time"]
        self.iv = attrs.get("iv")
        self.meta = attrs.get("meta", {})
        self.account = account

    def toJSON(self):
        return {
            "address": self.address,
            "file": {
                "name": self.file["name"],
                "type": self.file["type"],
                "size": self.file["size"],
            },
            "time": self.time,
            "iv": self.iv,
            "meta": self.meta,
        }

    def getFile(self, decrypt_progress_callback=print, download_progress_callback=print):
        # Implement your file retrieval logic here
        # You can use requests to download the file
        url = f"{self.account.Store.config['swarmGateway']}/bzz:/{self.address}/{self.file['name']}"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(self.file["name"], "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        download_progress_callback(len(chunk))
            decrypt_progress_callback("File downloaded successfully.")
            return self.file["name"]
        else:
            raise ValueError("Failed to download the file.")

    def saveAs(self, decrypt_progress_callback=print, download_progress_callback=print):
        file_path = self.getFile(decrypt_progress_callback, download_progress_callback)
        try:
            os.rename(file_path, self.file["name"])
            decrypt_progress_callback(f"File renamed to {self.file['name']}.")
        except Exception as e:
            decrypt_progress_callback(f"Error renaming the file: {str(e)}")

    def gatewayLink(self):
        return (
            f"{self.account.Store.config['swarmGateway']}/bzz:/{self.address}/{self.file['name']}"
        )

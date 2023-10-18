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
from typing import Dict

import requests
from ape.api.accounts import AccountAPI


class Hash:
    def __init__(self, config: Dict, attrs: Dict, account: AccountAPI):
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
        self.config = config

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

    def getFile(self):
        # Implement your file retrieval logic here
        # You can use requests to download the file
        url = f"{self.config['swarmGateway']}/bzz:/{self.address}/{self.file['name']}"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(self.file["name"], "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        print(len(chunk))  # noqa: ignore
            print("File downloaded successfully.")  # noqa: ignore
            return self.file["name"]
        else:
            raise ValueError("Failed to download the file.")

    def saveAs(self):
        file_path = self.getFile()
        try:
            os.rename(file_path, self.file["name"])
            print(f"File renamed to {self.file['name']}.")  # noqa: ignore
        except Exception as e:
            print(f"Error renaming the file: {str(e)}")  # noqa: ignore

    def gatewayLink(self):
        return f"{self.config['swarmGateway']}/bzz:/{self.address}/{self.file['name']}"

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

interact with bee API
"""
from typing import Dict, List, Union

import requests

from fds.utils.types import BatchId
from fds.utils.utils import (
    extract_upload_headers,
    make_collection_from_file_list,
    wrap_bytes_with_helpers,
)


class Bee:
    def __init__(self, url: str):
        self.url = url
        # self.headers = {"content-type": "application/octet-stream"}
        # self.gateWay = gateway

    def uploadData(
        self, postage_batch_id: Union[str, BatchId], data: str, options: Dict = {}
    ) -> str:
        self.headers = {
            "content-type": "application/octet-stream",
            **extract_upload_headers(postage_batch_id, options),
        }
        self.data = data
        self.response = requests.post(self.url + "/bytes", data=data, headers=self.headers)

        self.response_data = self.response.json()
        return self.response_data["reference"]

    def downloadData(self, swarmhash: str):
        self.headers = {
            "content-type": "application/octet-stream",
        }
        self.swarmhash = swarmhash

        self.response = requests.get(self.url + f"/bytes/{self.swarmhash}", headers=self.headers)

        if self.response.status_code == 200:
            self.binary_data = self.response.content
            return wrap_bytes_with_helpers(self.binary_data)
        else:
            print(f"Request failed with status code: {self.response.status_code}")  # noqa: ignore
            return

    def uploadFiles(
        self, postage_batch_id: Union[str, BatchId], file_list: List, options: Dict = {}
    ) -> str:
        self.headers = {
            "content-type": "application/octet-stream",
            **extract_upload_headers(postage_batch_id, options),
        }

        self.data = make_collection_from_file_list(file_list)  # type: ignore

        self.response = requests.post(self.url + "/bzz", data=self.data, headers=self.headers)

        self.response_data = self.response.json()
        return self.response_data["reference"]

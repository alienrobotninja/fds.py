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

handles
"""
import requests


class Message:
    def __init__(self, attrs, config, account):
        if "to" not in attrs:
            raise ValueError("to must be defined")
        if "from" not in attrs:
            raise ValueError("from must be defined")
        if "hash" not in attrs:
            raise ValueError("hash must be defined")

        self.config = config
        self.to = attrs["to"]
        self.from_ = attrs["from"]
        self.hash = attrs["hash"]
        self.account = account
        self.Mail = self.account.Mail

    def to_json(self):
        return {
            "to": self.to,
            "from": self.from_,
            "hash": self.hash.to_json(),
        }

    def get_file(self):
        if self.to.lower() == self.account.subdomain.lower():
            return self.Mail.receive(self.account, self)
        elif self.from_.lower() == self.account.subdomain.lower():
            return self.Mail.retrieve_sent(self.account)
        else:
            raise ValueError("There was a problem...")

    def get_file_url(self):
        return f"{self.config['beeGateway']}/bzz/{self.hash.get('address')}"

    def save_as(self):
        file = self.get_file()
        with open(file, "wb") as f:
            f.write(requests.get(self.get_file_url()).content)

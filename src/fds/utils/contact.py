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

handles Contract attributes
"""


class Contact:
    def __init__(self, attrs):
        if "subdomain" not in attrs:
            raise ValueError("subdomain must be defined")
        if "publicKey" not in attrs:
            raise ValueError("publicKey must be defined")
        if "multiboxAddress" not in attrs:
            raise ValueError("mailboxAddress must be defined")
        if "feedLocationHash" not in attrs:
            raise ValueError("feedLocationHash must be defined")

        self.subdomain = attrs["subdomain"]
        self.publicKey = attrs["publicKey"]
        self.multiboxAddress = attrs["multiboxAddress"]
        self.feedLocationHash = attrs["feedLocationHash"]

    def toJSON(self):
        return {
            "subdomain": self.subdomain,
            "publicKey": self.publicKey,
            "multiboxAddress": self.multiboxAddress,
            "feedLocationHash": self.feedLocationHash,
        }

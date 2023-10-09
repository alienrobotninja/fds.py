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
import os


class Utils:
    @staticmethod
    def file_to_buffer(file):
        if os.name == "nt":  # Windows
            with open(file, "rb") as f:
                return f.read()
        else:  # Unix-based systems (Linux, macOS)
            with open(file, "rb") as f:
                return f.read()

    @staticmethod
    def file_to_string(file):
        if os.name == "nt":  # Windows
            with open(file, "r") as f:
                return f.read()
        else:  # Unix-based systems (Linux, macOS)
            with open(file, "r") as f:
                return f.read()


if __name__ == "__main__":
    # Example usage:
    utils = Utils()

    buffer = utils.file_to_buffer("CHANGELOG.rst")
    string = utils.file_to_string("CHANGELOG.rst")
    print(string)
    print(buffer)

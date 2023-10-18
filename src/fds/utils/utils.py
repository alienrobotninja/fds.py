import json
from typing import Any, Dict, List


class CollectionItem:
    def __init__(self, path, data):
        self.path = path
        self.data = data


def make_file_path(file) -> str:
    if (
        hasattr(file, "webkitRelativePath")
        and file.webkitRelativePath
        and file.webkitRelativePath != ""
    ):
        return file.webkitRelativePath.split("/")[-1]

    if hasattr(file, "name") and file.name:
        return file.name

    raise TypeError("file is not a valid File object")


def make_collection_from_file_list(file_list) -> List[CollectionItem]:
    collection = []

    for file in file_list:
        if file:
            path = make_file_path(file)
            with open(file, "rb") as f:
                data = f.read()
            collection.append(CollectionItem(path, data))

    return collection


def wrap_bytes_with_helpers(data: bytes) -> Dict[str, Any]:
    return {
        "text": lambda: data.decode("utf-8"),
        "json": lambda: json.loads(data.decode("utf-8")),
        "hex": lambda: data.hex(),
    }


def extract_upload_headers(postage_batch_id: str, options: Dict = {}) -> Dict:
    if not postage_batch_id:
        raise Exception("Postage BatchID has to be specified!")

    headers = {"swarm-postage-batch-id": postage_batch_id}

    if options:
        if "pin" in options:
            headers["swarm-pin"] = str(options["pin"])

        if "encrypt" in options:
            headers["swarm-encrypt"] = str(options["encrypt"])

        if "tag" in options:
            headers["swarm-tag"] = str(options["tag"])

        if "deferred" in options and isinstance(options["deferred"], bool):
            headers["swarm-deferred-upload"] = str(options["deferred"])

    return headers

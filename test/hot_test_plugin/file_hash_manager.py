import os
import hashlib
import dataclasses
from typing import List


@dataclasses.dataclass
class FileHash:
    filepath: str
    hash: str

    @classmethod
    def from_filepath(cls, filepath: str):
        return get_file_hash(filepath)

    def __str__(self):
        return f"{self.filepath} : {self.hash}"


def get_file_hash(filepath: str) -> FileHash:
    if not os.path.exists(filepath):
        TypeError(f"Path does not exist: {filepath}. Cannot compute hash")
    with open(filepath, "r") as fp:
        file_content = fp.read()
        md5 = hashlib.md5(file_content.encode()).hexdigest()
        return FileHash(
            filepath=filepath,
            hash=md5,
        )


class HashManager:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hashes_filepath = f".{self.name}_hashes"

    def load(self):
        if not os.path.exists(self.hashes_filepath):
            return []

        with open(self.hashes_filepath, "r") as fp:
            lines = fp.readlines()

        file_hashes: List[FileHash]
        for line in lines:
            split = line.split(" ")
            hash = split[0]
            file_ = split[1]
            file_hashes.append(FileHash(filepath=file_, hash=hash))

    def save(self, filepaths):
        file_hashes: List[FileHash]
        for filepath in filepaths:
            file_hashes.append(get_file_hash(filepath))
        with open(self.hashes_filepath, "w") as fp:
            for file_hash in file_hashes:
                fp.write(f"{file_hash.filepath}{file_hash.hash}")

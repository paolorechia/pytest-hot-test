import os
import hashlib
import dataclasses
from hot_test_plugin import settings

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


def _get_test_filename(filepath: str) -> str:
    return (
        filepath
        .split("/")[-1]
        .replace(".py", ".txt")
    )

def _get_test_hash_filepath(filepath: str) -> str:
    _bootstrap_test_folder()
    test_folder = _get_test_folder()
    filename = _get_test_filename(filepath)
    test_hash_filepath = os.path.join(test_folder, filename)
    return test_hash_filepath

def _get_test_folder():
    return os.path.join(settings.PLUGIN_HASH_FOLDER, "test/")

def _get_source_folder():
    return os.path.join(settings.PLUGIN_HASH_FOLDER, "source/")

def _bootstrap_test_folder():
    if not os.path.exists(_get_test_folder()):
        os.makedirs(_get_test_folder())

def _bootstrap_source_folder():
    if not os.path.exists(_get_source_folder()):
        os.makedirs(_get_source_folder())

def get_test_file_hash(filepath: str) -> List[FileHash]:
    test_hash_filepath = _get_test_hash_filepath(filepath)
    if os.path.exists(test_hash_filepath):
        return read_hash_file(test_hash_filepath)
    return []

def save_test_file_hash(filepath: str, file_hash: FileHash):
    test_hash_filepath = _get_test_hash_filepath(filepath)
    save_hash_file(test_hash_filepath, [file_hash])

def read_hash_file(filepath: str) -> List[FileHash]:
    with open(filepath, "r") as fp:
        lines = fp.readlines()

    file_hashes: List[FileHash] = []
    for line in lines:
        split = line.split(" ")
        hash = split[0]
        file_ = split[1]
        file_hashes.append(FileHash(filepath=file_, hash=hash))
    return file_hashes

def save_hash_file(filepath: str, file_hashes: List[FileHash]):
    with open(filepath, "w") as fp:
        for file_hash in file_hashes:
            fp.write(f"{file_hash.hash} {file_hash.filepath}\n")

class HashManager:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hashes_filepath = f"{settings.PLUGIN_HASH_FOLDER}/{self.name}_hashes"
        self.hashes = []

    def load(self):
        if not os.path.exists(self.hashes_filepath):
            return []

        self.hashes = read_hash_file(self.hashes_filepath)

    def save(self, filepaths):
        file_hashes: List[FileHash] = []

        for filepath in filepaths:
            file_hashes.append(get_file_hash(filepath))

        save_hash_file(self.hashes_filepath, file_hashes)


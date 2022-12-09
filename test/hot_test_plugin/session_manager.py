from typing import Set, Dict
from hot_test_plugin import file_hash_manager


class SessionItemManager:
    """Test session state (singleton)

    Used to keep global state, such as which
    tests are not being executed because no changes
    were detected.
    """

    _ = None

    def __init__(self):
        self.ignore_paths = set()
        self.dependency_tracker: Dict[str, Set[str]] = {}

    @classmethod
    def as_singleton(cls):
        if cls._ is None:
            cls._ = cls()
        return cls._

    def add(self, path):
        self.ignore_paths.add(path)

    def add_dependency(self, test_path: str, dependencies: Set[str]):
        self.dependency_tracker[test_path] = dependencies


def get_sim() -> SessionItemManager:
    return SessionItemManager.as_singleton()

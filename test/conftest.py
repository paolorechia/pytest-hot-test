import pytest
import sys

class SessionItemManager:
    _ = None

    def __init__(self):
        self.ignore_paths = set()

    @classmethod
    def as_singleton(cls):
        if cls._ is None:
            cls._ = cls()
        return cls._

    def add(self, path):
        self.ignore_paths.add(path)

def pytest_sessionstart(session):
    sys.path.append("src")

def pytest_collection(session):
    print("Collection")

@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    print("Collection modifyitems")
    print("Config ", config)
    print("Items ", items)
    items = []
    print("Empty items ", items)
    return items


def pytest_ignore_collect(collection_path, path, config):
    print("Ignore collect", collection_path, path, config)
    SessionItemManager.as_singleton().add(str(path))
    return True

def pytest_collect_file(parent, file_path):
    print("Collect parent ", parent)
    print("Collect file ", file_path)
    if file_path == "test_mod1.py":
        print("BEEP")


def pytest_report_collectionfinish(config, start_path, startdir, items):
    print("Finished custom collection!")



def pytest_terminal_summary(terminalreporter: "TerminalReporter") -> None:
    tr = terminalreporter
    tr.write_sep("=", "Tests that were skipped by this plugin", yellow=True)
    tr.write_line("")
    for item in SessionItemManager.as_singleton().ignore_paths:
        tr.write_line(item)
    
    tr.write_line("Not too shabby :D", red=True)
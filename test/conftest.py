import pytest
import re
import sys
import os

# This should be settable through a config file / environment variable
SOURCE_CODE_ROOT = "src"

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
    sys.path.append(SOURCE_CODE_ROOT)

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
    print(collection_path)
    print(path)
    str_path = str(path)

    # Do not handle modules, e.g., let pytest expand on these paths
    if not str_path.endswith(".py"):
        return False

    with open(path, "r") as fp:
        source_code = fp.readlines()

    import_statements = [re.sub("\s+", " ", line) for line in source_code if "import" in line ]

    os.listdir(SOURCE_CODE_ROOT)

    dependencies_to_track = []
    for import_ in import_statements:
        imported_module_or_package = import_.split(" ")[1]
        print("Imported ", imported_module_or_package)
        dependencies_to_track.append(imported_module_or_package)

    # Can we find it in /src?
    dependencies = []

    list_files = list(os.walk(SOURCE_CODE_ROOT))
    for dep in dependencies_to_track:
        for root, dirs, files in list_files:
            # Is package? Then it should be a directory
            # if dep in dirs:
            
            print(root, dirs, files)


    SessionItemManager.as_singleton().add(str(path))



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
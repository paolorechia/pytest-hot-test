import pytest
import re
import sys
import os
from typing import List, Tuple, Set
import importlib
import inspect

# This should be settable through a config file / environment variable
SOURCE_CODE_ROOT = "src"


def get_imports_from_file(path: str) -> List[str]:
    with open(path, "r") as fp:
        source_code = fp.readlines()
    import_statements = [re.sub("\s+", " ", line) for line in source_code if "import" in line ]
    return import_statements


def find_dependencies_to_track(import_statements: List[str]):
    dependencies_to_track = []
    for import_ in import_statements:
        imported_module_or_package = import_.split(" ")[1]
        dependencies_to_track.append(imported_module_or_package)
    return dependencies_to_track

def find_artifacts_in_project(root: str, dependencies_to_track: List[str]) -> Tuple[List[str], List[str], List[str]]:
    modules = []
    packages = []
    files = []

    list_files = list(os.walk(root))
    for dep in dependencies_to_track:
        module_dep = dep + ".py"
        for root, dirs, files_ in list_files:
            package_name = re.sub(f"{root}/", "", root)
            if package_name == dep:
                packages.append(dep)
                files.append(os.path.join(root, package_name))

            if module_dep in files_:
                modules.append(module_dep)
                files.append(os.path.join(root, module_dep))
    return files, packages, modules


def absolute_path_to_root_relative_path(path: str) -> str:
    """Trims an absolute path to a relative path relative to the working directory.
    
    Example:
        path /Users/dev/pytest-hot-test/src/common/utils.py
        wd  /Users/dev/pytest-hot-test/
        Split  ['', 'src/common/utils.py']
        New files {'src/common/utils.py'}
    
    """
    wd = os.getcwd() + "/"
    split = path.split(wd)
    return split[1]


def find_referred_files(imported_modules) -> Set[str]:
    refererred_files = []
    for imported in imported_modules:
        member_keys = dir(imported)
        for key in member_keys:
            member = getattr(imported, key)
            try:
                used_file = inspect.getfile(member)
                refererred_files.append(used_file)
            except TypeError:
                pass
    return set(refererred_files)


def import_modules_from_files(root, files):
    imported_modules = []
    for file in files:
        importable = file.replace(f"{SOURCE_CODE_ROOT}/", "", -1).replace(".py", "")
        imported_modules.append(importlib.import_module(importable))
    return imported_modules

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

def pytest_ignore_collect(collection_path, path, config):
    str_path = str(path)

    # Do not handle modules, e.g., let pytest expand on these paths
    if not str_path.endswith(".py"):
        return False

    os.listdir(SOURCE_CODE_ROOT)

    import_statements = get_imports_from_file(str_path)
    dependencies_to_track = find_dependencies_to_track(import_statements)

    files, packages, modules = find_artifacts_in_project(SOURCE_CODE_ROOT, dependencies_to_track)

    relevant_files = set(files)
    print("Relevant files", relevant_files)

    imported_modules = import_modules_from_files(SOURCE_CODE_ROOT, relevant_files)
    referred_files = find_referred_files(imported_modules)
    print("Referred files ", referred_files)


    referred_files = set([absolute_path_to_root_relative_path(f) for f in referred_files])

    new_files = referred_files - relevant_files
    print("New files", new_files)

    SessionItemManager.as_singleton().add(str(path))



def pytest_terminal_summary(terminalreporter: "TerminalReporter") -> None:
    tr = terminalreporter
    tr.write_sep("=", "Tests that were skipped by this plugin", yellow=True)
    tr.write_line("")
    for item in SessionItemManager.as_singleton().ignore_paths:
        tr.write_line(item)
    
    tr.write_line("Not too shabby :D", red=True)
import pytest
import sys
import os

from typing import List, Optional

from hot_test_plugin import dependency_tracker as dtracker
from hot_test_plugin import session_manager
from hot_test_plugin import file_hash_manager
from hot_test_plugin import settings


def pytest_sessionstart(session):
    sys.path.append(settings.SOURCE_CODE_ROOT)


def pytest_ignore_collect(collection_path, path, config):
    """Main entry point of this plugin"""

    str_path = str(path)
    if "conftest.py" in str_path:
        return True

    # Do not handle modules, e.g., let pytest expand on these paths
    if not str_path.endswith(".py"):
        return False

    if "hot_test_plugin" in str_path:
        return True


    is_first_run = False
    is_source_changed = False
    is_test_changed = False

    sim = session_manager.get_sim()

    # State synchronization logic

    # Always load test file
    # --> Load old hash if it is available
    last_test_hash = file_hash_manager.get_test_file_hash(str_path)
    # --> Find new hash and compare
    test_hash: Optional[file_hash_manager.FileHash] = None
    if os.path.isfile(str_path):
        print(str_path)
        test_hash = file_hash_manager.FileHash.from_filepath(str_path)
        print("Current test hash ", test_hash)

    if not last_test_hash:
        is_first_run = True

    elif last_test_hash[0].hash != test_hash.hash:
        is_test_changed = True

    # --> Always save hash to disk
    file_hash_manager.save_test_file_hash(str_path, test_hash)


    # Always load dependencies
    # --> Load dependency list if they are available
    # --> Load old hashes if they are available
    # --> Find new hash and compare
    # --> Save hashes to disk
    relevant_files = dtracker.find_dependencies(collection_path, str_path, config)
    sim.add_dependency(str_path, relevant_files)

    # Fetch stored source file hashes
    old_source_files_hashes: List[
        file_hash_manager.FileHash
    ] = sim.source_files_hash_manager.load()

    # Cases that we need to think about:

    # New dependency, no point checking hash per hash
    old_files = set([fhash.filepath for fhash in old_source_files_hashes])
    print("Relevant files", relevant_files)
    print("Old files", old_files)
    if relevant_files != old_files:
        has_changes = True

    print("Relevant files", relevant_files)

    dependencies_hashes = []
    for source_file in relevant_files:
        if os.path.isfile(source_file):
            file_hash = file_hash_manager.FileHash.from_filepath(source_file)
            dependencies_hashes.append(file_hash)

    # In the first time, flag as True so we can proceed to save the hashes for the first time
    if not old_source_files_hashes:
        has_changes = True

    # TODO: always save hashes to disk
    for old_source_hash in old_source_files_hashes:
        for file_ in relevant_files:
            if old_source_hash.filepath == file_:
                pass


    if is_first_run:
        return False
    
    if is_source_changed:
        return False

    if is_test_changed:
        return False

    return True

    


def pytest_terminal_summary(terminalreporter: "TerminalReporter") -> None:
    """Adds a new section to the terminal reporter."""
    tr = terminalreporter
    tr.write_sep("=", "Tests dependencies tracked by 'hot-test' plugin", green=True)
    tr.write_line("")
    for key, item in session_manager.get_sim().dependency_tracker.items():
        tr.write_line(f"{key} ----depends on ----> {item}")

    tr.write_line("")

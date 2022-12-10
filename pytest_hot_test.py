# -*- coding: utf-8 -*-

import pytest
import sys
import os
from dataclasses import dataclass
from typing import List, Optional

from hot_test_plugin import settings
from hot_test_plugin import file_hash_manager
from hot_test_plugin import session_manager
from hot_test_plugin import dependency_tracker as dtracker
from hot_test_plugin import message_handler


def pytest_sessionstart(session):
    sys.path.append(settings.SOURCE_CODE_ROOT)
    message_handler.messages = []


@dataclass
class IgnoreResult:
    is_first_run: bool = False
    is_source_changed: bool = False
    is_test_changed: bool = False


def pytest_ignore_collect(collection_path, path, config):
    """Main entry point of this plugin"""

    str_path = str(path)
    if "conftest.py" in str_path:
        return True

    # Do not handle modules, e.g., let pytest expand on these paths
    if "test_" not in str_path:
        return True

    # Do not handle modules, e.g., let pytest expand on these paths
    if not str_path.endswith(".py"):
        return False

    if "hot_test_plugin" in str_path:
        return True

    result = IgnoreResult()

    sim = session_manager.get_sim()

    # State synchronization logic

    # Always load test file
    # --> Load old hash if it is available
    last_test_hash = file_hash_manager.get_test_file_hash(str_path)
    # --> Find new hash and compare
    test_hash: Optional[file_hash_manager.FileHash] = None
    if os.path.isfile(str_path):
        test_hash = file_hash_manager.FileHash.from_filepath(str_path)

    if not last_test_hash:
        result.is_first_run = True

    elif last_test_hash[0].hash != test_hash.hash:
        result.is_test_changed = True

    # --> Always save hash to disk
    file_hash_manager.save_test_file_hash(str_path, test_hash)

    # Find dependencies
    relevant_files = dtracker.find_dependencies(
        collection_path, str_path, config
    )
    sim.add_dependency(str_path, relevant_files)

    # Always pre-saved hash files
    # Fetch stored source file hashes

    # --> Load old hashes if they are available

    hmanager = file_hash_manager.HashManager(str_path)
    old_source_files_hashes: List[file_hash_manager.FileHash] = hmanager.load()

    # New dependency, no point checking hash per hash
    if not old_source_files_hashes:
        result.is_source_changed = True
    else:
        old_files = set([fhash.filepath for fhash in old_source_files_hashes])
        if relevant_files != old_files:
            result.is_source_changed = True

    # --> Find new hashes
    dependencies_hashes = []
    for source_file in relevant_files:
        if os.path.isfile(source_file):
            file_hash = file_hash_manager.FileHash.from_filepath(source_file)
            dependencies_hashes.append(file_hash)

    # --> Compare with old hashes
    # (Yikes, O(n^2)), but who cares at this point ;))
    if not result.is_source_changed:
        for old_source_hash in old_source_files_hashes:
            for new_source_hash in dependencies_hashes:
                if old_source_hash.filepath == new_source_hash.filepath:
                    if old_source_hash.hash != new_source_hash.hash:
                        result.is_source_changed = True
                        break

    # --> Save hashes to disk
    hmanager.save(dependencies_hashes)

    if result.is_first_run:
        return False

    if result.is_source_changed:
        return False

    if result.is_test_changed:
        return False

    return True


def pytest_terminal_summary(
    terminalreporter
) -> None:
    """Adds a new section to the terminal reporter."""
    tr = terminalreporter
    if settings.DEBUG:
        tr.write_sep(
            "*",
            "Debug messages",
            yellow=True
        )

    for message in message_handler.messages:
        for elem in message:
            tr.write(str(elem))
        tr.write_line("")
    tr.write_sep(
        "=",
        "Tests dependencies tracked by 'hot-test' plugin",
        green=True
    )
    tr.write_line("")
    for key, item in session_manager.get_sim().dependency_tracker.items():
        tr.write_line(f"{key} ----depends on ----> {item}")

    tr.write_line("")


def pytest_addoption(parser):
    group = parser.getgroup("hot-test")
    group.addoption(
        "--foo",
        action="store",
        dest="dest_foo",
        default="2022",
        help='Set the value for the fixture "bar".',
    )

    parser.addini("HELLO", "Dummy pytest.ini setting")


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo

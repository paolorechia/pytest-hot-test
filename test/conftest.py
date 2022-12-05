import pytest
import sys

from hot_test_plugin import dependency_tracker as dtracker
from hot_test_plugin import session_manager

def pytest_sessionstart(session):
    sys.path.append(dtracker.SOURCE_CODE_ROOT)

def pytest_ignore_collect(collection_path, path, config):
    """Main entry point of this plugin"""

    str_path = str(path)
    if "conftest.py" in str_path:
        return True

    if "hot_test_plugin" in str_path:
        return True

    relevant_files = dtracker.find_dependencies(collection_path, str_path, config)
    sim = session_manager.get_sim()
    sim.add_dependency(str_path, relevant_files)


def pytest_terminal_summary(terminalreporter: "TerminalReporter") -> None:
    """Adds a new section to the terminal reporter."""
    tr = terminalreporter
    tr.write_sep("=", "Tests dependencies tracked by 'hot-test' plugin", green=True)
    tr.write_line("")
    for key, item in session_manager.get_sim().dependency_tracker.items():
        tr.write_line(f"{key} ----depends on ----> {item}")

    tr.write_line("")

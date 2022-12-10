import os

PLUGIN_HASH_FOLDER = ".pytest-hot-cache"
SOURCE_CODE_ROOT = os.environ.get("PYTEST_HOT_TEST_SOURCE_ROOT", os.getcwd())
MAX_ITER_SAFETY = 1000
DEBUG = os.environ.get("PYTEST_HOT_TEST_DEBUG_MODE", "")

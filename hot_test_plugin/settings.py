import os

PLUGIN_HASH_FOLDER = ".pytest-hot-cache"
SOURCE_CODE_ROOT = os.environ.get("PYTEST_HOT_TEST_SOURCE_ROOT", ".")
MAX_ITER_SAFETY = 1000
DEBUG = False

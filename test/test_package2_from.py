import pytest

import inspect
from package2 import mod4

@pytest.mark.skip("Case not yet handled")
def test_hello():
    assert mod4.hello_mod_4()



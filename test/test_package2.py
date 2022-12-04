import pytest
import inspect
import package2.mod4

@pytest.mark.skip("Case not yet handled")
def test_hello():
    assert package2.mod4.hello_mod_4()



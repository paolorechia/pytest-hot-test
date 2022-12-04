import pytest
import inspect
import package3.package4.mod5

@pytest.mark.skip("Case not yet handled")
def test_hello():
    assert package3.package4.mod5.hello_mod5()



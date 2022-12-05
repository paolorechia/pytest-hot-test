import pytest
import inspect
import package1


def test_hello():
    assert package1.mod3.hello_mod_3()

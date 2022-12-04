import inspect
import mod1

def test_hello():
    assert mod1.hello_world() == "Hello"
    f = inspect.getsourcefile(mod1.hello_world)
    print(f)

def test_hello2():
    assert mod1.hello_world() == "Hello"
    f = inspect.getsourcefile(mod1.hello_world)
    print(f)
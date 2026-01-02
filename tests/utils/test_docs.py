from __future__ import annotations

import pytest

from template.utils._docs import copy_doc
from template.utils.logs import verbose


def test_copy_doc_function() -> None:
    """Test decorator to copy docstring on functions."""

    # test copy of docstring
    def foo(x, y) -> None:
        """My doc."""

    @copy_doc(foo)
    def foo2(x, y) -> None:
        pass

    @copy_doc(foo)
    def foo3(x, y) -> None:
        """Doc of foo3."""

    assert foo.__doc__ == foo2.__doc__
    assert foo.__doc__ + "Doc of foo3." == foo3.__doc__

    # test copy of docstring from a function without docstring
    def foo(x, y) -> None:
        pass

    with pytest.raises(RuntimeError, match="The docstring from foo could not"):

        @copy_doc(foo)
        def foo2(x, y) -> None:
            pass

    # test copy docstring of decorated function
    @verbose
    def foo(verbose=None) -> None:
        """My doc."""

    @copy_doc(foo)
    def foo2(verbose=None) -> None:
        pass

    @copy_doc(foo)
    @verbose
    def foo3(verbose=None) -> None:
        pass

    assert foo.__doc__ == foo2.__doc__
    assert foo.__doc__ == foo3.__doc__


def test_copy_doc_class():
    """Test decorator to copy docstring on classes."""

    class Foo:
        """My doc."""

        def __init__(self) -> None:
            pass

        def method1(self) -> None:
            """Super 101 doc."""

    @copy_doc(Foo)
    class Foo2:
        def __init__(self) -> None:
            pass

        @copy_doc(Foo.method1)
        def method2(self) -> None:
            pass

        @copy_doc(Foo.method1)
        @verbose
        def method3(self, verbose=None) -> None:
            pass

        @staticmethod
        @copy_doc(Foo.method1)
        @verbose
        def method4(verbose=None) -> None:
            pass

    assert Foo.__doc__ == Foo2.__doc__
    assert Foo.method1.__doc__ == Foo2.method2.__doc__
    assert Foo.method1.__doc__ == Foo2.method3.__doc__
    assert Foo.method1.__doc__ == Foo2.method4.__doc__
    foo = Foo()
    foo2 = Foo2()
    assert foo.__doc__ == foo2.__doc__
    assert foo.method1.__doc__ == foo2.method2.__doc__
    assert foo.method1.__doc__ == foo2.method3.__doc__
    assert foo.method1.__doc__ == foo2.method4.__doc__

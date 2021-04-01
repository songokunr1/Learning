import pytest
import fastcache
from Algorytmy import exercise

# @pytest.fixture(scope='module')
# def test_setup():
#     print('setup')
#     yield 50
#     print('teardown')

@pytest.mark.parametrize("n, expected_value", [(0, 0), (1, 1), (2, 1), (3, 2),(10,55), (-1, None)])
def test_fib(n, expected_value):
    value = exercise.fib(n)
    assert value == expected_value

@pytest.mark.parametrize("n, expected_value", [(0, 0), (1, 1), (2, 1), (3, 2),(10,55), (-1, None)])
def test_fib_iter(n, expected_value):
    value = exercise.fib_iter(n)
    print('next function')
    assert value == expected_value

@pytest.mark.parametrize("n, expected_value", [(0, 0), (1, 1), (2, 1), (3, 2),(10,55), (-1, None)])
def test_fib_memory(n, expected_value):
    value = exercise.fib_memory(n)
    assert value == expected_value

@pytest.mark.parametrize("n, expected_value", [(0, 1), (1, 1), (2, 2), (12, 479001600), (10, 3628800), (-1, None)])
def test_silnia(n, expected_value):
    value = exercise.silnia(n)
    assert value == expected_value

@pytest.mark.parametrize("n, expected_value", [(0, 1), (1, 1), (2, 2), (12, 479001600), (10, 3628800), (-1, None)])
def test_silnia(n, expected_value):
    value = exercise.silnia_iter(n)
    assert value == expected_value
import example
import pytest
import sys


@pytest.mark.skipif(sys.version_info > (2, 7), reason="nie wiem")
@pytest.mark.number
def test_add():
    assert example.add(5, 3) == 8
    assert example.add(2, 3) == 5
    assert example.add(1, 3) == 4


@pytest.mark.number
def test_product():
    assert example.product(5, 5) == 25
    assert example.product(2, 5) == 10


@pytest.mark.string
def test_string():
    result = example.add('Hello', ' Word')
    assert result == 'Hello Word'
    assert type(result) is str


@pytest.mark.parametrize('x, y, result', [
    (7, 3, 10),
    ('Hello', ' Word', 'Hello Word'),
    (10.5, 25.5, 36)])
def test_add_few_times(x, y, result):
    assert example.add(x, y) == result

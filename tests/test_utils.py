import pytest

from forth import utils

from fractions import Fraction

from numbers import Number


def test_tokenize() -> None:
    assert utils.tokenize('1 1 + 3 * . CR') == ['1', '1', '+', '3', '*', '.', 'CR']
    assert utils.tokenize(' 1 -1 2 -10   9') == ['1', '-1', '2', '-10', '9']


def test_strip_trailing_comment() -> None:
    assert utils.strip_trailing_comment(' foo # bar') == ' foo '
    assert utils.strip_trailing_comment(' # this has only comments') == ' '


@pytest.mark.parametrize(
    'token, expect',
    [
        ('1', 1),
        ('-42', -42),
        ('2.123', 2.123),
        ('2.5+4.1j', complex(2.5, 4.1)),
        ('1/2', Fraction(1, 2)),
        ('0xABC', 0xABC),
        ('0b10110', 0b10110),
    ],
)
def test_parse_utils(token: str, expect: Number) -> None:
    assert utils.parse_number(token) == expect

import pytest

import forth

import decimal

from numbers import Number


def test_eval_token0() -> None:
    vm = forth.VM()

    # NOTE: not registering any functions. forth.VM is pretty useless.
    assert vm.stack == []

    vm.eval_token('1')
    vm.eval_token('1')
    assert vm.stack == [1, 1]

    with pytest.raises(decimal.InvalidOperation):
        vm.eval_token('+')


def test_eval_token1() -> None:
    vm = forth.VM()
    vm.env.register('+', forth.op_add)

    assert vm.stack == []

    vm.eval_token('1')

    assert vm.stack == [1]

    vm.eval_token('1')

    assert vm.stack == [1, 1]


def test_eval_token2() -> None:
    vm = forth.VM()
    vm.env.register('+', forth.op_add)
    vm.eval_token('1')
    vm.eval_token('1')
    vm.eval_token('1')
    vm.eval_token('+')
    assert vm.stack == [1, 2]


def test_eval_token3() -> None:
    vm = forth.VM()
    vm.env.register('+', forth.op_add)
    vm.eval_token('-1')
    vm.eval_token('-4')
    vm.eval_token('+')
    assert vm.stack == [-5]


def test_tokenize() -> None:
    assert forth.tokenize('1 1 + 3 * . CR') == ['1', '1', '+', '3', '*', '.', 'CR']
    assert forth.tokenize(' 1 -1 2 -10   9') == ['1', '-1', '2', '-10', '9']


@pytest.mark.parametrize(
    'line,expect',
    [
        ('1', [1]),
        ('1 234 5', [1, 234, 5]),
        ('1 1 +', [2]),
        ('1 -1 +', [0]),
        ('5 1 1 +', [5, 2]),
        ('1 1 + 1', [2, 1]),
        ('10.21 2.13 +', [decimal.Decimal('12.34')]),
    ],
)
def test_eval(line: str, expect: list[Number]) -> None:
    vm = forth.VM()
    vm.env.register('+', forth.op_add)

    vm.eval_line(line)

    assert vm.stack == expect


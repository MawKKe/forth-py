import pytest

import decimal

from numbers import Number

import forth
from forth.forth import tokenize


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
    vm.register_op('+', forth.ops.op_add)

    assert vm.stack == []

    vm.eval_token('1')

    assert vm.stack == [1]

    vm.eval_token('1')

    assert vm.stack == [1, 1]


def test_eval_token2() -> None:
    vm = forth.VM()
    vm.register_op('+', forth.ops.op_add)
    vm.eval_token('1')
    vm.eval_token('1')
    vm.eval_token('1')
    vm.eval_token('+')
    assert vm.stack == [1, 2]


def test_eval_token3() -> None:
    vm = forth.VM()
    vm.register_op('+', forth.ops.op_add)
    vm.eval_token('-1')
    vm.eval_token('-4')
    vm.eval_token('+')
    assert vm.stack == [-5]


def test_tokenize() -> None:
    assert tokenize('1 1 + 3 * . CR') == ['1', '1', '+', '3', '*', '.', 'CR']
    assert tokenize(' 1 -1 2 -10   9') == ['1', '-1', '2', '-10', '9']


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
    vm.register_op('+', forth.ops.op_add)

    vm.eval_line(line)

    assert vm.stack == expect


def test_func_def_and_call() -> None:
    prog = """
    : MUL2 2 * ;
    1 MUL2 MUL2 MUL2 MUL2 MUL2 MUL2 MUL2 MUL2
    """
    vm = forth.VM()

    assert not vm.env.keys()

    vm.register_op('*', forth.ops.op_mul)

    assert set(vm.env.keys()) == {'*'}

    vm.eval(prog)

    assert vm.stack == [256]
    assert set(vm.env.keys()) == {'*', 'MUL2'}


def test_ops_cr(capfdbinary) -> None:  # type: ignore
    vm = forth.VM()
    vm.register_op('CR', forth.ops.op_cr)
    vm.eval_token('CR')
    out, err = capfdbinary.readouterr()
    assert out == b'\n'
    assert err == b''

    vm.eval('CR CR')
    out, err = capfdbinary.readouterr()
    assert out == b'\n\n'
    assert err == b''


def test_ops_print(capfdbinary) -> None:  # type: ignore
    vm = forth.VM()
    vm.register_op('+', forth.ops.op_add)
    vm.register_op('.', forth.ops.op_print)
    vm.eval('1 1 + .')
    out, err = capfdbinary.readouterr()
    assert out == b'2'
    assert err == b''


if __name__ == '__main__':
    import sys

    sys.exit(pytest.main(['-v']))

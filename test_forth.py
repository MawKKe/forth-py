import pytest

import forth

import decimal


def test_handle_token0():
    vm = forth.VM()

    # NOTE: not registering any functions. forth.VM is pretty useless.
    assert vm.stack == []

    vm.handle_token('1')
    vm.handle_token('1')
    assert vm.stack ==[1, 1]

    with pytest.raises(decimal.InvalidOperation):
        vm.handle_token('+')


def test_handle_token1():
    vm = forth.VM()
    vm.env.register('+', 2, 1, forth.op_add)

    assert vm.stack == []

    vm.handle_token('1')

    assert vm.stack == [1]

    vm.handle_token('1')

    assert vm.stack == [1, 1]


def test_handle_token2():
    vm = forth.VM()
    vm.env.register('+', 2, 1, forth.op_add)
    vm.handle_token('1')
    vm.handle_token('1')
    vm.handle_token('1')
    vm.handle_token('+')
    assert vm.stack == [1, 2]


def test_handle_token3():
    vm = forth.VM()
    vm.env.register('+', 2, 1, forth.op_add)
    vm.handle_token('-1')
    vm.handle_token('-4')
    vm.handle_token('+')
    assert vm.stack == [-5]


def test_stack_split():
    assert forth.stack_split([], 0) == ([], [])
    assert forth.stack_split([1,2,3], 0) == ([1,2,3], [])
    assert forth.stack_split([1,2,3], 1) == ([1, 2], [3])
    assert forth.stack_split([1,2,3,4,5], 2) == ([1,2,3], [4,5])


def test_tokenize():
   assert forth.tokenize('1 1 + 3 * . CR') == ['1', '1', '+', '3', '*', '.', 'CR']
   assert forth.tokenize(' 1 -1 2 -10   9') == ['1', '-1', '2', '-10', '9']
   

@pytest.mark.parametrize('line,expect', [
    ('1', [1]),
    ('1 234 5', [1, 234, 5]),
    ('1 1 +', [2]),
    ('1 -1 +', [0]),
    ('5 1 1 +', [5, 2]),
    ('1 1 + 1', [2, 1]),
    ('10.21 2.13 +', [decimal.Decimal('12.34')]),
])
def test_eval(line, expect):
    vm = forth.VM()
    vm.env.register('+', 2, 1, forth.op_add)

    vm.eval_line(line)

    assert vm.stack == expect


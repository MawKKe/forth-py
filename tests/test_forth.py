from fractions import Fraction

import pytest

import forth


def test_eval_noenv() -> None:
    vm = forth.VM()

    # NOTE: not registering any functions. forth.VM is pretty useless.
    assert vm.stack() == []
    vm.eval_string('1 42 2/3')

    assert vm.stack() == [1, 42, Fraction(2, 3)]

    with pytest.raises(ValueError, match='Invalid token'):
        vm.eval_string('+')


def test_pop() -> None:
    vm = forth.VM()
    vm.eval_string('1 2 3 4 5 6')
    assert vm.stack() == [1, 2, 3, 4, 5, 6]

    assert vm.pop(0) == []
    assert vm.stack() == [1, 2, 3, 4, 5, 6]

    assert vm.pop(1) == [6]
    assert vm.stack() == [1, 2, 3, 4, 5]

    assert vm.pop(2) == [4, 5]
    assert vm.stack() == [1, 2, 3]

    with pytest.raises(ValueError):
        assert len(vm.stack()) < 4
        _ = vm.pop(4)


def test_func_def_and_call() -> None:
    prog = """
    : MUL2 2 * ;
    1 MUL2 MUL2 MUL2 MUL2 MUL2 MUL2 MUL2 MUL2
    """
    vm = forth.VM()

    assert not vm.env().keys()

    vm.register_op('*', forth.ops.op_mul)

    assert set(vm.env().keys()) == {'*'}

    vm.eval_token_stream(forth.gen_tokens(prog))

    assert vm.stack() == [256]
    assert set(vm.env().keys()) == {'*', 'MUL2'}


def test_counters() -> None:  # type: ignore
    vm = forth.VM()
    forth.ops.register_default_ops(vm)
    assert vm.get_counters().num_tokens == 0
    vm.eval_string('1 1 +')
    assert vm.get_counters().num_tokens == 3
    vm.eval_string(': fun 20 * 3 + ;')
    vm.eval_string('7 + fun')
    assert vm.get_counters().num_tokens == 17
    assert vm.stack() == [183]

    ctr = vm.get_counters()
    ctr.num_tokens += 1  # get_counters() returns a copy
    assert vm.get_counters().num_tokens == 17


def test_string_handling(capfdbinary) -> None:  # type: ignore
    vm = forth.VM()
    forth.ops.register_default_ops(vm)
    vm.eval_string('1 1 + . CR @"hello world!" . CR')
    out, err = capfdbinary.readouterr()
    assert err == b''
    assert out == b'2\nhello world!\n'

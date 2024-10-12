import forth
import forth.ops

import pytest
import sys


@pytest.mark.parametrize(
    'op, prog, expect',
    [
        (forth.ops.op_add, '1 1', 2),
        (forth.ops.op_sub, '1 1', 0),
        (forth.ops.op_mul, '3 2', 6),
        (forth.ops.op_div, '10 2', 5),
        (forth.ops.op_pow, '2 5', 32),
    ],
)
def test_arith_ops(op, prog, expect) -> None:  # type: ignore
    vm = forth.VM()
    vm.eval_string(prog)
    op(vm)
    assert vm.stack() == [expect]


def test_nop() -> None:  # type: ignore
    vm = forth.VM()
    assert vm.stack() == []
    assert vm.env() == {}

    forth.ops.op_nop(vm)

    assert vm.stack() == []
    assert vm.env() == {}

    vm.eval_string('1 2 3')
    assert vm.stack() == [1, 2, 3]
    assert vm.env() == {}

    forth.ops.op_nop(vm)

    assert vm.stack() == [1, 2, 3]
    assert vm.env() == {}


@pytest.mark.parametrize(
    'setup,op,after',
    [
        ('1', forth.ops.op_dup, [1, 1]),
        ('2 3', forth.ops.op_dup_n, [2, 2, 2]),
        ('4 5', forth.ops.op_flip, [5, 4]),
        ('6 7', forth.ops.op_drop, [6]),
    ],
)
def test_stack_manip(setup, op, after) -> None:  # type: ignore
    vm = forth.VM()
    vm.eval_string(setup)
    before = vm.stack()
    op(vm)
    assert vm.stack() != before
    assert vm.stack() == after


def test_assert() -> None:  # type: ignore
    vm = forth.VM()
    vm.eval_string('1')
    forth.ops.op_assert(vm)
    vm.eval_string('0')
    with pytest.raises(AssertionError, match=f'value={0}'):
        forth.ops.op_assert(vm)


def test_io(capfdbinary) -> None:  # type: ignore
    vm = forth.VM()
    forth.ops.op_cr(vm)
    out, err = capfdbinary.readouterr()
    assert err == b''
    assert out == b'\n'

    forth.ops.op_cr(vm)
    forth.ops.op_cr(vm)
    out, err = capfdbinary.readouterr()
    assert err == b''
    assert out == b'\n\n'

    vm.eval_string('42')
    forth.ops.op_print(vm)
    out, err = capfdbinary.readouterr()
    assert err == b''
    assert out == b'42'

    msg = b'hello'
    vm.eval_token_stream([str(c) for c in msg])
    vm.eval_token_stream([f'{len(msg)}'])
    forth.ops.op_writeb(vm)
    sys.stdout.buffer.flush()
    out, err = capfdbinary.readouterr()
    assert err == b''
    assert out == msg


def test_register_default_ops() -> None:  # type: ignore
    vm = forth.VM()
    assert len(vm.env()) == 0
    forth.ops.register_default_ops(vm)
    assert len(vm.env()) != 0


def test_halt() -> None:  # type: ignore
    vm = forth.VM()
    vm.register_op('+', forth.ops.op_add)
    assert vm.stack() == []
    assert list(vm.env().items()) == [('+', forth.ops.op_add)]
    assert not vm.is_halted()

    vm.eval_string('1 1 +')
    assert vm.stack() == [2]
    assert list(vm.env().items()) == [('+', forth.ops.op_add)]
    assert not vm.is_halted()

    forth.ops.op_halt(vm)
    assert vm.stack() == [2]
    assert list(vm.env().items()) == [('+', forth.ops.op_add)]
    assert vm.is_halted()

    vm.eval_string('1 2 3 4')  # should not do anything since we are halted
    assert vm.stack() == [2]
    assert list(vm.env().items()) == [('+', forth.ops.op_add)]
    assert vm.is_halted()


@pytest.mark.parametrize(
    'op, args, expect',
    [
        (forth.ops.op_lt, '1 1', False),
        (forth.ops.op_lt, '1 2', True),
        (forth.ops.op_le, '1 1', True),
        (forth.ops.op_le, '1 2', True),
        (forth.ops.op_gt, '1 1', False),
        (forth.ops.op_gt, '2 1', True),
        (forth.ops.op_ge, '1 1', True),
        (forth.ops.op_ge, '2 1', True),
        (forth.ops.op_and, '1 1', True),
        (forth.ops.op_and, '1 0', False),
        (forth.ops.op_and, '0 0', False),
        (forth.ops.op_or, '1 0', True),
        (forth.ops.op_or, '0 1', True),
        (forth.ops.op_or, '0 0', False),
        (forth.ops.op_eq, '1 1', True),
        (forth.ops.op_eq, '0 1', False),
        (forth.ops.op_not, '1', False),
        (forth.ops.op_not, '0', True),
    ],
)
def test_logical_ops(op, args, expect) -> None:  # type: ignore
    vm = forth.VM()
    vm.eval_string(args)
    op(vm)
    assert vm.stack() == [expect]

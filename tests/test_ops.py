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
    vm.eval(prog)
    op(vm)
    assert vm.stack == [expect]


def test_nop() -> None:  # type: ignore
    vm = forth.VM()
    assert vm.stack == []
    assert vm.env == {}

    forth.ops.op_nop(vm)

    assert vm.stack == []
    assert vm.env == {}

    vm.eval('1 2 3')

    assert vm.stack == [1, 2, 3]
    assert vm.env == {}

    forth.ops.op_nop(vm)

    assert vm.stack == [1, 2, 3]
    assert vm.env == {}


def test_stack_manip() -> None:  # type: ignore
    vm = forth.VM()
    vm.eval('1')
    assert vm.stack == [1]
    forth.ops.op_dup(vm)
    assert vm.stack == [1, 1]

    vm = forth.VM()
    vm.eval('2 3')
    assert vm.stack == [2, 3]
    forth.ops.op_flip(vm)
    assert vm.stack == [3, 2]


def test_assert() -> None:  # type: ignore
    vm = forth.VM()
    vm.eval('1')
    forth.ops.op_assert(vm)
    vm.eval('0')
    with pytest.raises(AssertionError, match=f'value={0}'):
        forth.ops.op_assert(vm)


def test_io(capfdbinary) -> None:  # type: ignore
    vm = forth.VM()
    forth.ops.op_cr(vm)
    out, err = capfdbinary.readouterr()
    assert err == b''
    assert out == b'\n'

    vm.eval('42')
    forth.ops.op_print(vm)
    out, err = capfdbinary.readouterr()
    assert err == b''
    assert out == b'42'

    msg = b'hello'
    vm.eval_tokens([str(c) for c in reversed(msg)])
    vm.eval_token(f'{len(msg)}')
    forth.ops.op_writeb(vm)
    sys.stdout.buffer.flush()
    out, err = capfdbinary.readouterr()
    assert err == b''
    assert out == msg


def test_register_default_ops() -> None:  # type: ignore
    vm = forth.VM()
    assert len(vm.env) == 0
    forth.ops.register_default_ops(vm)
    assert len(vm.env) != 0


def test_halt() -> None:  # type: ignore
    vm = forth.VM()
    vm.register_op('+', forth.ops.op_add)
    assert vm.stack == []
    assert list(vm.env.items()) == [('+', forth.ops.op_add)]
    assert not vm.is_halted()

    vm.eval('1 1 +')
    assert vm.stack == [2]
    assert list(vm.env.items()) == [('+', forth.ops.op_add)]
    assert not vm.is_halted()

    forth.ops.op_halt(vm)
    assert vm.stack == [2]
    assert list(vm.env.items()) == [('+', forth.ops.op_add)]
    assert vm.is_halted()

    vm.eval('1 2 3 4')  # should not do anything since we are halted
    assert vm.stack == [2]
    assert list(vm.env.items()) == [('+', forth.ops.op_add)]
    assert vm.is_halted()

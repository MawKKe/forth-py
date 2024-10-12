import sys
import operator
import typing as t
from forth import VM

BinOp = t.Callable[[t.Any, t.Any], t.Any]


def generic_binop(vm: VM, op: BinOp) -> None:
    [lhs, rhs] = vm.pop(2)
    vm.push(op(lhs, rhs))


def op_writeb(vm: VM) -> None:
    [n] = vm.pop()
    bv = bytes(vm.pop(n))
    sys.stdout.buffer.write(bv)


# Basic arithmetic
def op_add(vm: VM) -> None:
    generic_binop(vm, operator.add)


def op_sub(vm: VM) -> None:
    generic_binop(vm, operator.sub)


def op_mul(vm: VM) -> None:
    generic_binop(vm, operator.mul)


def op_pow(vm: VM) -> None:
    generic_binop(vm, operator.pow)


def op_div(vm: VM) -> None:
    generic_binop(vm, operator.truediv)


# Logical ops
def op_lt(vm: VM) -> None:
    generic_binop(vm, operator.lt)


def op_le(vm: VM) -> None:
    generic_binop(vm, operator.le)


def op_gt(vm: VM) -> None:
    generic_binop(vm, operator.gt)


def op_ge(vm: VM) -> None:
    generic_binop(vm, operator.ge)


def op_eq(vm: VM) -> None:
    generic_binop(vm, operator.eq)


def op_and(vm: VM) -> None:
    generic_binop(vm, operator.and_)


def op_or(vm: VM) -> None:
    generic_binop(vm, operator.or_)


def op_not(vm: VM) -> None:
    [val] = vm.pop()
    vm.push(operator.not_(val))


# IO
def op_cr(_: VM) -> None:
    print()


def op_dup(vm: VM) -> None:
    [value] = vm.pop()
    vm.push(value, value)


def op_dup_n(vm: VM) -> None:
    [value, n] = vm.pop(2)
    data = [value] * n
    vm.push(*data)


def op_print(vm: VM) -> None:
    [val] = vm.pop()
    print(val, end='')


def op_nop(_: VM) -> None:
    return


def op_flip(vm: VM) -> None:
    [lhs, rhs] = vm.pop(2)
    vm.push(rhs, lhs)


def op_drop(vm: VM) -> None:
    _ = vm.pop(1)


def op_assert(vm: VM) -> None:
    [value] = vm.pop()
    assert value, f'value={value}, stack={vm.stack}'


def op_halt(vm: VM) -> None:
    vm.halt()


def register_default_ops(vm: VM) -> VM:
    vm.register_op('HALT', op_halt)

    vm.register_op('NOP', op_nop)

    vm.register_op('+', op_add)
    vm.register_op('-', op_sub)
    vm.register_op('*', op_mul)
    vm.register_op('/', op_div)
    vm.register_op('POW', op_pow)

    vm.register_op('<', op_lt)
    vm.register_op('>', op_gt)
    vm.register_op('<=', op_le)
    vm.register_op('>=', op_ge)
    vm.register_op('==', op_eq)
    vm.register_op('AND', op_and)
    vm.register_op('OR', op_or)
    vm.register_op('NOT', op_not)

    vm.register_op('DUP', op_dup)
    vm.register_op('DUPN', op_dup_n)
    vm.register_op('FLIP', op_flip)
    vm.register_op('DROP', op_drop)

    vm.register_op('.', op_print)
    vm.register_op('WRITEB', op_writeb)
    vm.register_op('CR', op_cr)

    vm.register_op('ASSERT', op_assert)
    return vm

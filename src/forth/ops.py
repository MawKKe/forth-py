import sys

from forth import VM


def op_writeb(vm: VM) -> None:
    [n] = vm.pop()
    bv = bytes(vm.pop(n))
    sys.stdout.buffer.write(bv)


def op_add(vm: VM) -> None:
    [lhs, rhs] = vm.pop(2)
    vm.push(lhs + rhs)


def op_sub(vm: VM) -> None:
    [lhs, rhs] = vm.pop(2)
    vm.push(lhs - rhs)


def op_mul(vm: VM) -> None:
    [lhs, rhs] = vm.pop(2)
    vm.push(lhs * rhs)


def op_pow(vm: VM) -> None:
    [lhs, rhs] = vm.pop(2)
    vm.push(lhs**rhs)


def op_div(vm: VM) -> None:
    [lhs, rhs] = vm.pop(2)
    vm.push(lhs / rhs)


def op_cr(_: VM) -> None:
    print()


def op_dup(vm: VM) -> None:
    [value] = vm.pop()
    vm.push(value, value)


def op_print(vm: VM) -> None:
    [val] = vm.pop()
    print(val, end='')


def op_nop(_: VM) -> None:
    return


def op_flip(vm: VM) -> None:
    [lhs, rhs] = vm.pop(2)
    vm.push(rhs, lhs)


def op_assert(vm: VM) -> None:
    [value] = vm.pop()
    assert value, f'value={value}, stack={vm.stack}'


def op_halt(vm: VM) -> None:
    vm.halt()


def register_default_ops(vm: VM) -> VM:
    vm.register_op('WRITEB', op_writeb)
    vm.register_op('+', op_add)
    vm.register_op('-', op_sub)
    vm.register_op('*', op_mul)
    vm.register_op('/', op_div)
    vm.register_op('pow', op_pow)
    vm.register_op('nop', op_nop)
    vm.register_op('flip', op_flip)
    vm.register_op('CR', op_cr)
    vm.register_op('DUP', op_dup)
    vm.register_op('dup', op_dup)
    vm.register_op('assert', op_assert)
    vm.register_op('.', op_print)
    vm.register_op('halt', op_halt)
    return vm

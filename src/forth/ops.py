import sys

from forth import VM


def op_writeb(vm: VM) -> None:
    n = vm.stack.pop()
    vm._assert_stack('op_writeb', n)
    bv = bytes(vm.pop(n))
    sys.stdout.buffer.write(bv)


def op_add(vm: VM) -> None:
    vm._assert_stack('op_add', 2)
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs + rhs)


def op_sub(vm: VM) -> None:
    vm._assert_stack('op_sub', 2)
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs - rhs)


def op_mul(vm: VM) -> None:
    vm._assert_stack('op_mul', 2)
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs * rhs)


def op_pow(vm: VM) -> None:
    vm._assert_stack('op_pow', 2)
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs**rhs)


def op_div(vm: VM) -> None:
    vm._assert_stack('op_div', 2)
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs / rhs)


def op_cr(_: VM) -> None:
    print()


def op_dup(vm: VM) -> None:
    vm._assert_stack('op_dup', 1)
    vm.stack.append(vm.stack[-1])


def op_print(vm: VM) -> None:
    vm._assert_stack('op_print', 1)
    val = vm.stack.pop()
    print(val, end='')


def op_nop(_: VM) -> None:
    return


def op_flip(vm: VM) -> None:
    vm._assert_stack('op_flip', 2)
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.extend([rhs, lhs])


def op_assert(vm: VM) -> None:
    vm._assert_stack('op_assert', 1)
    value = vm.stack.pop()
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

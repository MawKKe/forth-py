import shlex

import sys
from pathlib import Path

import decimal

import typing as t
from dataclasses import dataclass, field

from functools import partial

import argparse


def tokenize(line: str) -> list[str]:
    return shlex.split(line.strip())


Op = t.Callable[['VM'], None]


@dataclass
class VM:
    stack: list = field(default_factory=list)
    env: dict[str, Op] = field(default_factory=dict)

    def register_op(self, token: str, op: Op) -> None:
        self.env[token] = op

    def eval_token(self, tok: str) -> None:
        op = self.env.get(tok)

        if op is None:
            value = decimal.Decimal(tok)
            self.stack.append(value)
            return

        op(self)

    def eval_tokens(self, tokens: list[str]) -> None:
        for tok in tokens:
            self.eval_token(tok)

    def eval(self, content: str) -> None:
        for line in content.splitlines():
            self.eval_line(line)

    def eval_line(self, line: str) -> None:
        tokens = tokenize(line.strip())

        if not tokens:
            return

        if tokens[0] == ':':
            assert tokens[-1] == ';'
            _, name, *body, _ = tokens
            self.register_op(name, partial(VM.eval_tokens, tokens=body))

        else:
            self.eval_tokens(tokens)


def op_writeb(vm: VM) -> None:
    n = vm.stack.pop()
    for _ in range(int(n)):
        b = vm.stack.pop()
        assert 0 <= b <= 0xFF
        sys.stdout.buffer.write(bytes([int(b)]))


def op_add(vm: VM) -> None:
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs + rhs)


def op_sub(vm: VM) -> None:
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs - rhs)


def op_mul(vm: VM) -> None:
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs * rhs)


def op_div(vm: VM) -> None:
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs / rhs)


def op_cr(_: VM) -> None:
    print()


def op_dup(vm: VM) -> None:
    vm.stack.append(vm.stack[-1])


def op_print(vm: VM) -> None:
    val = vm.stack.pop()
    print(val, end='')


def make_default_vm() -> VM:
    vm = VM()
    vm.register_op('WRITEB', op_writeb)
    vm.register_op('+', op_add)
    vm.register_op('-', op_sub)
    vm.register_op('*', op_mul)
    vm.register_op('/', op_div)
    vm.register_op('CR', op_cr)
    vm.register_op('DUP', op_dup)
    vm.register_op('.', op_print)
    return vm


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog=argv[0])
    p.add_argument('sources', nargs='+', type=Path)
    args = p.parse_args(argv[1:])
    vm = make_default_vm()

    for src in args.sources:
        vm.eval(src.read_text())

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

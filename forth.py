import shlex

import sys
from pathlib import Path

import decimal

import typing as t 
from dataclasses import dataclass, field

from functools import partial

@dataclass
class Env:
    ops: dict = field(default_factory=dict)

    def get(self, tok: str):
        return self.ops.get(tok, None)

    def register(self, tok: str, callable: t.Callable):
        self.ops[tok] = callable

@dataclass
class VM:
    stack: list = field(default_factory=list)
    env: Env = field(default_factory=Env)

    def eval_token(self, tok: str):
        op = self.env.get(tok)

        if op is None:
            value = decimal.Decimal(tok)
            self.stack.append(value)
            return

        op(self)


    def eval_tokens(self, tokens: list):
        for tok in tokens:
            self.eval_token(tok)

    def eval(self, content: str):
        for line in content.splitlines():
            self.eval_line(line)

    def eval_line(self, line: str):
        tokens = tokenize(line.strip())

        if not tokens:
            return

        if tokens[0] == ':':
            assert tokens[-1] == ';'
            _, name, *body, _ = tokens
            self.env.register(name, partial(VM.eval_tokens, tokens=body))

        else:
            self.eval_tokens(tokens)



def tokenize(line: str) -> list[str]:
    return shlex.split(line.strip())


def stack_split(stack, n):
    if n == 0:
        return stack, []
    return stack[:-n], stack[-n:]


def op_add(vm: VM):
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs + rhs)

def op_sub(vm: VM):
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs - rhs)

def op_mul(vm: VM):
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs * rhs)

def op_div(vm: VM):
    rhs = vm.stack.pop()
    lhs = vm.stack.pop()
    vm.stack.append(lhs / rhs)

def op_cr(_: VM):
    print()

def op_dup(vm: VM):
    vm.stack.append(vm.stack[-1])

def op_print(vm: VM):
    val = vm.stack.pop()
    print(val, end='')

def make_default_vm():
    vm = VM()
    vm.env.register('+', op_add)
    vm.env.register('-', op_sub)
    vm.env.register('*', op_mul)
    vm.env.register('/', op_div)
    vm.env.register('CR', op_cr)
    vm.env.register('DUP', op_dup)
    vm.env.register('.', op_print)
    return vm

def main():
    content = Path(sys.argv[1]).read_text('utf8')
    vm = make_default_vm()
    vm.eval(content)

if __name__ == '__main__':
    main()


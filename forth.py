import shlex

import sys
from pathlib import Path

import typing as t 
from dataclasses import dataclass, field


@dataclass
class Env:
    ops: dict[str, tuple[int, int, t.Callable]] = field(default_factory=dict)

    def get(self, tok: str):
        return self.ops.get(tok, None)

    def register(self, tok: str, n_args: int, n_ret: int, callable: t.Callable):
        self.ops[tok] = (n_args, n_ret, callable)

@dataclass
class VM:
    stack: list = field(default_factory=list)
    env: Env = field(default_factory=Env)

    def handle_token(self, tok: str):
        op = self.env.get(tok)

        if op is None:
            self.stack = self.stack + [tok]
            return

        n_args, n_ret, callable = op

        stack, args = stack_split(self.stack, n_args)

        res = callable(*args)

        new = [res] if n_ret else []

        self.stack = stack + new

    def eval(self, content: str):
        for line in content.splitlines():
            self.eval_line(line)

    def eval_line(self, line: str):
        line = line.strip()
        for tok in tokenize(line):
            self.handle_token(tok)


def tokenize(line: str) -> list[str]:
    return shlex.split(line.strip())


def stack_split(stack, n):
    if n == 0:
        return stack, []
    return stack[:-n], stack[-n:]


def op_add(arg1, arg2):
    return int(arg1) + int(arg2)

def op_sub(arg1, arg2):
    return int(arg1) - int(arg2)

def op_mul(arg1, arg2):
    return int(arg1) * int(arg2)

def op_div(arg1, arg2):
    return int(arg1) / int(arg2)

def op_cr():
    print()

def op_print(arg):
    print(arg, end='')

def make_default_vm():
    vm = VM()
    vm.env.register('+', 2, 1, op_add)
    vm.env.register('-', 2, 1, op_sub)
    vm.env.register('*', 2, 1, op_mul)
    vm.env.register('/', 2, 1, op_div)
    vm.env.register('CR', 0, 0, op_cr)
    vm.env.register('.', 1, 0, op_print)
    return vm

def main():
    content = Path(sys.argv[1]).read_text('utf8')
    vm = make_default_vm()
    vm.eval(content)

if __name__ == '__main__':
    main()


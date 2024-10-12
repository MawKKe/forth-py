import fractions
import shlex
import typing as t
from dataclasses import dataclass, field

from functools import partial


def tokenize(line: str) -> list[str]:
    return shlex.split(line.strip())


def strip_trailing_comment(line: str, commend_sep: str = '#') -> str:
    return line.split(sep=commend_sep, maxsplit=1)[0]


Op = t.Callable[['VM'], None]


@dataclass
class VM:
    stack: list = field(default_factory=list)
    env: dict[str, Op] = field(default_factory=dict)

    def pop(self, n: int = 1) -> list:
        if n == 0:
            return []
        self.stack, res = self.stack[:-n], self.stack[-n:]
        return res

    def status(self) -> int:
        return len(self.stack)

    def _assert_stack(self, opname: str, need_elems: int) -> None:
        assert (
            len(self.stack) >= need_elems
        ), f'Op "{opname}" needs at least {need_elems} elems, have: {self.stack}'

    def register_op(self, token: str, op: Op) -> None:
        self.env[token] = op

    def parse_number(self, tok: str) -> t.Optional[t.Any]:
        if '.' in tok:
            return float(tok)
        if '/' in tok:
            return fractions.Fraction(tok)
        if 'j' in tok:
            return complex(tok)
        if tok.startswith('0x'):
            return int(tok[2:], 16)
        if tok.startswith('0b'):
            return int(tok[2:], 2)
        return int(tok)

    def eval_token(self, tok: str) -> None:
        if op := self.env.get(tok):
            op(self)
            return

        if (val := self.parse_number(tok)) is not None:
            self.stack.append(val)
            return

        raise ValueError(f'Invalid token: {tok}')

    def eval_tokens(self, tokens: list[str]) -> None:
        for tok in tokens:
            self.eval_token(tok)

    def eval(self, content: str) -> None:
        for line in content.splitlines():
            self.eval_line(line)

    def eval_line(self, line: str) -> None:
        line = strip_trailing_comment(line).strip()

        tokens = tokenize(line.strip())

        if not tokens:
            return

        if tokens[0] == ':':
            assert tokens[-1] == ';'
            _, name, *body, _ = tokens
            self.register_op(name, partial(VM.eval_tokens, tokens=body))

        else:
            self.eval_tokens(tokens)

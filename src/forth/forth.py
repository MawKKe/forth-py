import typing as t
from dataclasses import dataclass, field

from functools import partial

from . import utils


Op = t.Callable[['VM'], None]


@dataclass
class VM:
    stack: list = field(default_factory=list)
    env: dict[str, Op] = field(default_factory=dict)

    def pop(self, n: int = 1) -> list:
        if n == 0:
            return []
        if n > len(self.stack):
            raise ValueError(f'pop(n={n}) requested, stack only has {len(self.stack)} elems')
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

    def eval_token(self, tok: str) -> None:
        if op := self.env.get(tok):
            op(self)
            return

        if (val := utils.parse_number(tok)) is not None:
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
        line = utils.strip_trailing_comment(line).strip()

        tokens = utils.tokenize(line.strip())

        if not tokens:
            return

        if tokens[0] == ':':
            assert tokens[-1] == ';'
            _, name, *body, _ = tokens
            self.register_op(name, partial(VM.eval_tokens, tokens=body))

        else:
            self.eval_tokens(tokens)

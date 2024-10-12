import typing as t
from dataclasses import dataclass, field

from functools import partial

from . import utils


Op = t.Callable[['VM'], None]


@dataclass
class VM:
    stack: list = field(default_factory=list)
    env: dict[str, Op] = field(default_factory=dict)
    _halted: bool = False

    def is_halted(self) -> bool:
        return self._halted

    def halt(self) -> None:
        self._halted = True

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

    def eval_token_stream(self, stream: t.Iterable[str]) -> None:
        func: list[str] = []
        in_func_def = False
        for tok in stream:
            if self.is_halted():
                return
            if tok == ':':
                assert not in_func_def, 'Already inside function definition'
                in_func_def = True
                continue
            if tok == ';':
                assert in_func_def, 'Spurious semicolon?'
                self.register_op(func[0], partial(VM.eval_token_stream, stream=func[1:]))
                func = []
                in_func_def = False
                continue

            if in_func_def:
                func.append(tok)
                continue

            if op := self.env.get(tok):
                op(self)
                continue

            if (val := utils.parse_number(tok)) is not None:
                self.stack.append(val)
                continue

            raise ValueError(f'Invalid token: {tok}')

    def eval_string(self, source: str) -> None:
        self.eval_token_stream(utils.gen_tokens(source))

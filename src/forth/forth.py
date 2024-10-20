import typing as t
from dataclasses import dataclass, field, replace
from functools import partial

from . import utils

Op = t.Callable[['VM'], None]


@dataclass
class Counters:
    num_tokens: int = 0

    def tick_tokens(self) -> None:
        self.num_tokens += 1


@dataclass
class VM:
    _stack: list = field(default_factory=list)
    _env: dict[str, Op] = field(default_factory=dict)
    _halted: bool = False
    _counters: Counters = field(default_factory=Counters)

    def stack(self) -> list:
        return list(self._stack)

    def env(self) -> dict:
        return dict(self._env)

    def is_halted(self) -> bool:
        return self._halted

    def halt(self) -> None:
        self._halted = True

    def pop(self, n: int = 1) -> list:
        if n == 0:
            return []
        if n > len(self._stack):
            raise ValueError(f'pop(n={n}) requested, stack only has {len(self._stack)} elems')
        self._stack, res = self._stack[:-n], self._stack[-n:]
        return res

    def push(self, *values) -> None:  # type: ignore
        self._stack.extend(values)

    def status(self) -> int:
        return len(self._stack)

    def register_op(self, token: str, op: Op) -> None:
        self._env[token] = op

    def lookup_op(self, name: str) -> t.Optional[Op]:
        return self._env.get(name)

    def eval_token_stream(self, stream: t.Iterable[str]) -> None:
        func: list[str] = []
        in_func_def = False
        for tok in stream:
            if self.is_halted():
                return
            self._counters.tick_tokens()
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

            if len(tok) > 1 and tok[0] == '@':
                self.push(tok[1:])
                continue

            if in_func_def:
                func.append(tok)
                continue

            if op := self.lookup_op(tok):
                op(self)
                continue

            if (val := utils.parse_number(tok)) is not None:
                self._stack.append(val)
                continue

            raise ValueError(f'Invalid token: {tok}')

    def eval_string(self, source: str) -> None:
        self.eval_token_stream(utils.gen_tokens(source))

    def get_counters(self) -> Counters:
        return replace(self._counters)

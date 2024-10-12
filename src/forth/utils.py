import shlex
import fractions
import typing as t
import io


def gen_tokens_from_line_iterable(file: t.Iterable) -> t.Iterator[str]:
    for line in file:
        line = strip_trailing_comment(line).strip()
        yield from shlex.split(line.strip())


def gen_tokens(source: str) -> t.Iterator[str]:
    return gen_tokens_from_line_iterable(io.StringIO(source))


def strip_trailing_comment(line: str, commend_sep: str = '#') -> str:
    return line.split(sep=commend_sep, maxsplit=1)[0]


def parse_number(tok: str) -> t.Optional[t.Any]:
    try:
        if 'j' in tok:
            return complex(tok)
        if '.' in tok:
            return float(tok)
        if '/' in tok:
            return fractions.Fraction(tok)
        if tok.startswith('0x'):
            return int(tok[2:], 16)
        if tok.startswith('0b'):
            return int(tok[2:], 2)
        return int(tok)
    except ValueError:
        return None

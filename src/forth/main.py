import sys
from pathlib import Path
import argparse
import typing as t

import forth


def chain_files(files: list) -> t.Iterator[str]:
    for file in files:
        yield from forth.gen_tokens_from_line_iterable(file)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog=Path(argv[0]).name)
    p.add_argument('sources', nargs='+', metavar='src', type=argparse.FileType('r'))
    args = p.parse_args(argv[1:])

    vm = forth.VM()
    vm = forth.ops.register_default_ops(vm)

    token_stream = chain_files(args.sources)

    vm.eval_token_stream(token_stream)

    return vm.status()


# set as entrypoint in [project.scripts]
def cli() -> None:  # pragma: no cover
    sys.exit(main(sys.argv))


if __name__ == '__main__':
    cli()

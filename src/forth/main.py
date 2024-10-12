import sys
from pathlib import Path
import argparse
import typing as t

import forth


def chain_files(open_files: list) -> t.Iterator[str]:
    for file in open_files:
        yield from forth.gen_tokens_from_line_iterable(file)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog=Path(argv[0]).name)
    p.add_argument('-c', type=str, dest='inline_src', metavar='inline-src')
    p.add_argument('file_src', metavar='file-src', nargs='*', type=argparse.FileType('r'))
    p.add_argument('--show-stats', action='store_true')
    args = p.parse_args(argv[1:])

    vm = forth.VM()
    vm = forth.ops.register_default_ops(vm)

    if args.inline_src and args.file_src:
        print(
            'error: inline source (-c) and file source(s) specified at the same time',
            file=sys.stderr,
        )
        return -2

    if args.inline_src:
        vm.eval_string(args.inline_src)
    elif args.file_src:
        token_stream = chain_files(args.file_src)

        vm.eval_token_stream(token_stream)
    else:
        print('error: no sources provided', file=sys.stderr)
        return -1

    if args.show_stats:
        print('# counters:', vm.get_counters())

    return vm.status()


# set as entrypoint in [project.scripts]
def cli() -> None:  # pragma: no cover
    sys.exit(main(sys.argv))


if __name__ == '__main__':
    cli()

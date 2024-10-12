import sys
from pathlib import Path
import argparse

import forth


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog=Path(argv[0]).name)
    p.add_argument('sources', nargs='+', metavar='src', type=argparse.FileType('r'))
    args = p.parse_args(argv[1:])

    vm = forth.VM()
    vm = forth.ops.register_default_ops(vm)

    for src in args.sources:
        vm.eval(src.read())

    return vm.status()


# set as entrypoint in [project.scripts]
def cli() -> None:  # pragma: no cover
    sys.exit(main(sys.argv))


if __name__ == '__main__':
    cli()

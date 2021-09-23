import argparse
import sys
from pathlib import Path

from img2texture import img2tex
from ._constants import __version__ as version, __copyright__ as copyright


def print_version():
    print(f'img2texture {version} {copyright}')


class ParsedArgs:
    def __init__(self):
        if "--version" in sys.argv:
            print_version()
            exit(0)

        parser = argparse.ArgumentParser()

        parser.add_argument("-m", "--mix",
                            type=float,
                            default=0.2)
        parser.add_argument("source",
                            help="Path of source image file.")
        parser.add_argument("target",
                            help="Path of target (tile) file.")
        parser.add_argument('--version',
                            action='store_true',
                            default=False,
                            help="Show version info and exit")

        self._parsed = parser.parse_args()

    @property
    def source(self) -> Path:
        return Path(self._parsed.source)

    @property
    def target(self) -> Path:
        return Path(self._parsed.target)

    @property
    def mix(self) -> float:
        return self._parsed.mix


def cli():
    args = ParsedArgs()
    img2tex(args.source, args.target, pct=args.mix)

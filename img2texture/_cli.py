import argparse
from pathlib import Path

from img2texture import img2tex


class ParsedArgs:
    def __init__(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("-m", "--mix",
                            type=float,
                            default=0.2)
        parser.add_argument("source",
                            help="Path of source image file.")
        parser.add_argument("target",
                            help="Path of target (tile) file.")

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

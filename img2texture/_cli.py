import argparse
import os
import sys
from enum import Enum
from pathlib import Path

from img2texture import img2tex
import img2texture._constants as constants

# import __version__ as version, __copyright__ as copyright
from ._tiling import tile


def print_version():
    print(f'img2texture {constants.__version__} {constants.__copyright__}')


class Mode(Enum):
    both = "both"
    none = "none"


def confirm(message: str) -> bool:
    while True:
        answer = input(f"{message} (y/n) ").upper()
        if answer.startswith("Y"):
            return True
        if answer.startswith("N"):
            return False


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
                            help="Path of the converted file.")
        parser.add_argument("--tile",
                            action='store_true',
                            default=False,
                            help="Create an additional file with four copies "
                                 "of the converted image merged side by side")
        parser.add_argument("--mode",
                            choices=[str(m.value) for m in Mode],
                            default=Mode.both)
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

    @property
    def mode(self) -> Mode:
        return Mode(self._parsed.mode)

    @property
    def tile(self) -> bool:
        return self._parsed.tile


def tile_filename(texture: Path) -> Path:
    basename = texture.name
    basename = basename.rpartition('.')[0]
    basename += "_2x2.jpg"
    return texture.parent / basename


def cli():
    args = ParsedArgs()

    if args.target.exists():
        if not confirm(f"File '{args.target.name}' exists. Overwrite?"):
            exit(3)
        os.remove(args.target)

    img2tex(args.source, args.target, pct=args.mix)

    if args.tile:
        tile_src = args.target if args.mode != Mode.none else args.source
        tile_fn = tile_filename(tile_src)
        if not confirm(f"File '{tile_fn}' exists. Overwrite?"):
            exit(3)

        if tile_fn.exists():
            os.remove(tile_fn)
        tile(tile_src, tile_fn, horizontal=2, vertical=2)

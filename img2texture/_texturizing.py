# SPDX-FileCopyrightText: (c) 2021 Artёm iG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import warnings
from math import floor
from pathlib import Path
from typing import Tuple, Union

from PIL import Image  # importing with tweaked options


# todo Find a way to add dithering noise to 8-bit grading
#
# It looks like in 2021 Pillow cannot alpha-blend 16-bit or 32-bit images.
# So we need to keep our gradient mask in 8 bit.
#
# To avoid banding, we may want to create 16 or 32 bit gradient, and then
# convert it to dithered 8-bit version. But it seems, Pillow cannot do such
# conversion either (https://github.com/python-pillow/Pillow/issues/3011)
#
# So all colors are 8 bit now. Maybe we should find a way to add some random
# noise to out gradient. But Pillow will not create noise, we need to generate
# it pixel-by-pixel, and probably not in Python (numpy could do this)


def horizontal_gradient_256_scaled(size: Tuple[int, int],
                                   reverse=True) -> Image:
    gradient = Image.new('L', (256, 1), color=None) # type: ignore
    for x in range(256):
        if reverse:
            gradient.putpixel((x, 0), x)
        else:
            gradient.putpixel((x, 0), 255 - x)

    return gradient.resize(size)


def vertical_gradient_256_scaled(size: Tuple[int, int], reverse=True) -> Image:
    gradient = Image.new('L', (1, 256), color=None) # type: ignore
    for x in range(256):
        if reverse:
            gradient.putpixel((0, x), x)
        else:
            gradient.putpixel((0, x), 255 - x)

    return gradient.resize(size)


def stripe_size(full_size: int, pct: float) -> int:
    if not 0 <= pct <= 0.5:
        raise ValueError(pct)
    result = floor(full_size * pct)
    assert result * 2 <= full_size
    return result


class Mixer:
    def __init__(self, source: Image, pct=1.0 / 3):
        self.source = source
        self.pct = pct

    @property
    def src_width(self) -> int:
        return self.source.size[0]

    @property
    def src_height(self) -> int:
        return self.source.size[1]

    @property
    def horizontal_stripe_width(self) -> int:
        return stripe_size(self.src_width, self.pct)

    @property
    def vertical_stripe_height(self) -> int:
        return stripe_size(self.src_height, self.pct)

    def _left_stripe_image(self):
        return self.source.crop(
            (0, 0, self.horizontal_stripe_width, self.src_height))

    def _right_stripe_image(self):
        return self.source.crop((
            self.src_width - self.horizontal_stripe_width, 0, self.src_width,
            self.src_height))

    def _bottom_stripe_image(self):
        return self.source.crop((
            0, self.src_height - self.vertical_stripe_height, self.src_width,
            self.src_height))

    @staticmethod
    def _to_rgba(image: Image) -> Image:
        if image.mode != 'RGBA':
            converted = image.convert('RGBA')
            assert converted is not None
            return converted
        return image

    def make_seamless_h(self) -> Image:
        stripe = self._to_rgba(self._right_stripe_image())
        stripe.putalpha(
            horizontal_gradient_256_scaled(stripe.size, reverse=False))

        overlay = Image.new('RGBA', size=self.source.size, color=0x00)
        overlay.paste(stripe, box=(0, 0))

        comp = Image.alpha_composite(self._to_rgba(self.source), overlay)

        comp = comp.crop(
            (0, 0, comp.size[0] - self.horizontal_stripe_width, comp.size[1]))
        return comp

    def make_seamless_v(self) -> Image:
        stripe = self._to_rgba(self._bottom_stripe_image())
        stripe.putalpha(
            vertical_gradient_256_scaled(stripe.size, reverse=False))

        overlay = Image.new('RGBA', size=self.source.size, color=0x00)
        overlay.paste(stripe, box=(0, 0))

        comp = Image.alpha_composite(self._to_rgba(self.source), overlay)

        comp = comp.crop(
            (0, 0, comp.size[0], comp.size[1] - self.vertical_stripe_height))
        return comp


def img2tex(src: Path, dst: Path, pct=0.25):
    warnings.warn("Replaced by `file_to_seamless`", DeprecationWarning,
                  stacklevel=2)
    file_to_seamless(src, dst, overlap=pct)


Overlap = Union[float, Tuple[float, float]]


def file_to_seamless(src: Path, dst: Path, overlap: Overlap = 0.25) -> None:
    """Reads image from `src` file, converts it to seamless tile and saves
    to `dst` file."""
    image_to_seamless(Image.open(src), overlap=overlap).save(dst)


def image_to_seamless(src: Image, overlap: Overlap = 0.25) -> Image:
    """Converts `PIL.Image` to seamless `PIL.Image`."""
    mixer1 = Mixer(src, pct=_horizontal_overlap(overlap))
    result = mixer1.make_seamless_h()

    mixer2 = Mixer(result, pct=_vertical_overlap(overlap))
    result = mixer2.make_seamless_v()
    if result.mode != "RGB":
        result = result.convert("RGB")
    return result


def _float_or_index(dynamic: Overlap, idx: int) -> float:
    if isinstance(dynamic, float):
        return dynamic
    else:
        return dynamic[idx]


def _horizontal_overlap(overlaps: Overlap) -> float:
    return _float_or_index(overlaps, 0)


def _vertical_overlap(overlaps: Overlap) -> float:
    return _float_or_index(overlaps, 1)

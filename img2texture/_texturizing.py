# SPDX-FileCopyrightText: (c) 2021 Artyom Galkin <github.com/rtmigo>
# SPDX-License-Identifier: MIT
from pathlib import Path
from typing import Tuple

from PIL import Image


def gradient256h(size: Tuple[int, int], lr=True) -> Image:
    gradient = Image.new('L', (256, 1), color=0x00)
    for x in range(256):
        if lr:
            gradient.putpixel((x, 0), x)
        else:
            gradient.putpixel((x, 0), 255 - x)

    return gradient.resize(size)


def gradient256v(size: Tuple[int, int], lr=True) -> Image:
    gradient = Image.new('L', (1, 256), color=0x00)
    for x in range(256):
        if lr:
            gradient.putpixel((0, x), x)
        else:
            gradient.putpixel((0, x), 255 - x)

    return gradient.resize(size)


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
        return round(self.src_width * self.pct)

    @property
    def vertical_stripe_height(self) -> int:
        return round(self.src_height * self.pct)

    def _left_stripe_image(self):
        return self.source.crop(
            (0, 0, self.horizontal_stripe_width, self.src_height))

    def _right_stripe_image(self):
        return self.source.crop(
            (self.src_width - self.horizontal_stripe_width, 0,
             self.src_width, self.src_height))

    def _bottom_stripe_image(self):
        return self.source.crop(
            (0, self.src_height - self.vertical_stripe_height,
             self.src_width, self.src_height))

    def _to_rgba(self, image: Image) -> Image:
        if image.mode != 'RGBA':
            converted = image.convert('RGBA')
            assert converted is not None
            return converted
        return image

    def make_seamless_h(self) -> Image:
        stripe = self._to_rgba(self._right_stripe_image())
        stripe.putalpha(gradient256h(stripe.size, lr=False))

        overlay = Image.new('RGBA', size=self.source.size, color=0x00)
        overlay.paste(stripe, box=(0, 0))

        comp = Image.alpha_composite(self._to_rgba(self.source),
                                     overlay)

        comp = comp.crop((0,
                          0,
                          comp.size[0] - self.horizontal_stripe_width,
                          comp.size[1]))
        return comp

    def make_seamless_v(self) -> Image:
        stripe = self._to_rgba(self._bottom_stripe_image())
        stripe.putalpha(gradient256v(stripe.size, lr=False))

        overlay = Image.new('RGBA', size=self.source.size, color=0x00)
        overlay.paste(stripe, box=(0, 0))

        comp = Image.alpha_composite(self._to_rgba(self.source),
                                     overlay)

        comp = comp.crop((0,
                          0,
                          comp.size[0],
                          comp.size[1] - self.vertical_stripe_height))
        return comp


def img2tex(src: Path, dst: Path, pct=0.25):
    mixer1 = Mixer(Image.open(src), pct=pct)
    result = mixer1.make_seamless_h()

    mixer2 = Mixer(result, pct=pct)
    result = mixer2.make_seamless_v()
    result.save(dst)

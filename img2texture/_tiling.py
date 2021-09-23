# SPDX-FileCopyrightText: (c) 2021 Artyom Galkin <github.com/rtmigo>
# SPDX-License-Identifier: MIT

from pathlib import Path

from ._common import Image  # importing with tweaked options


def tile(source: Path, target: Path,
         horizontal: int = 3, vertical: int = 3) -> None:
    """Merges multiple copies of `source` image into the `target` image
    side-by-side."""
    image = Image.open(source)

    w, h = image.size
    total_width = w * horizontal
    total_height = h * vertical

    new_im = Image.new('RGB', (total_width, total_height))

    for x in range(horizontal):
        for y in range(vertical):
            new_im.paste(image, (w * x, h * y))

    new_im.save(target)

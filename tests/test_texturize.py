# SPDX-FileCopyrightText: (c) 2021 Artёm iG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import unittest
from pathlib import Path

from PIL import Image

from img2texture._texturizing import horizontal_gradient_256_scaled, Mixer, \
    file_to_seamless
from img2texture._tiling import tile
from tests.helpers import temp_file_path, file_md5


class TestGradient(unittest.TestCase):
    def test(self):
        w = 100
        h = 50
        result = horizontal_gradient_256_scaled((100, 50))
        self.assertEqual(result.size[0], w)
        self.assertEqual(result.size[1], h)

        outfile = temp_file_path("gradient_h_1.png")
        result.save(outfile)
        self.assertEqual(file_md5(outfile), 'b135a054bc325a37df404b141f512567')


class TestToSeamless(unittest.TestCase):
    def test_overlap_tuple(self):
        src = Path(__file__).parent / "data" / "sand.png"
        dst = temp_file_path("sand-tx-tuple.png")
        dst_tiled = temp_file_path("sand-tx-tuple-tiled.png")

        file_to_seamless(src, dst, overlap=(0.4, 0.3))
        tile(dst, dst_tiled)

        # without RGB conversion it was c9c4d278498050e99c1df3994efc3bcd
        self.assertEqual(file_md5(dst), '696749d1337dc3d9e4021e9b8852a6e1')

    def test_overlap_float(self):
        src = Path(__file__).parent / "data" / "sand.png"
        dst = temp_file_path("sand-tx-float.png")
        dst_tiled = temp_file_path("sand-tx-float-tiled.png")

        file_to_seamless(src, dst, overlap=0.4)
        tile(dst, dst_tiled)

        # without RGB conversion it was c9c4d278498050e99c1df3994efc3bcd
        self.assertEqual(file_md5(dst), 'c957847053bc9f7747369f8a3ae091d2')


if __name__ == "__main__":
    # TestGradient().test()
    TestToSeamless().test_overlap_tuple()

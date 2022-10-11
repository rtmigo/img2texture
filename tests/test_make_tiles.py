# SPDX-FileCopyrightText: (c) 2021 Artsiom iG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import os
import unittest
from pathlib import Path

from tests.helpers import file_md5, temp_file_path
from img2texture._tiling import tile


class TestMakeTiles(unittest.TestCase):
    def test(self):
        src = Path(__file__).parent / "data" / "sand.png"
        dst = temp_file_path("sand-9x9.tmp.png")

        assert "tmp" in str(dst)
        if dst.exists():
            os.remove(dst)

        tile(src, dst)

        self.assertEqual(file_md5(dst), '5da5f36aac37ca80d07ea6ef319d8723')


if __name__ == "__main__":
    TestMakeTiles().test()

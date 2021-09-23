import unittest
from pathlib import Path

from PIL import Image

from tests.helpers import temp_file_path, file_md5
from textu.texturizing import gradient256h, Mixer
from textu.tiling import tile


class TestGradient(unittest.TestCase):
    def test(self):
        w = 100
        h = 50
        result = gradient256h((100, 50))
        self.assertEqual(result.size[0], w)
        self.assertEqual(result.size[1], h)

        outfile = temp_file_path("gradient_h_1.png")
        result.save(outfile)
        self.assertEqual(file_md5(outfile), 'b135a054bc325a37df404b141f512567')


class TestMyTextu(unittest.TestCase):
    def test_both(self):
        src = Path(__file__).parent / "data" / "sand.png"
        dst = temp_file_path("sand-tx.png")
        dst_tiled = temp_file_path("sand-tx-tiled.png")

        pct = 0.4

        mixer1 = Mixer(Image.open(src), pct=pct)
        result = mixer1.make_seamless_h()

        mixer2 = Mixer(result, pct=pct)
        result = mixer2.make_seamless_v()
        result.save(dst)

        tile(dst, dst_tiled)


if __name__ == "__main__":
    # TestGradient().test()
    TestMyTextu().test_both()

# SPDX-FileCopyrightText: (c) 2021 Artёm iG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import hashlib
import os
from pathlib import Path


def temp_file_path(basename: str) -> Path:
    result = Path(__file__).parent / "data" / "out" / basename
    if result.exists():
        os.remove(result)
    result.parent.mkdir(exist_ok=True)
    return result


def file_md5(fname: Path) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 16), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

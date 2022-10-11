import datetime
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import PyInstaller.__main__ as compile
import click
import neatest
from chkpkg import Package


@click.group()
def app():
    pass


@app.command()
def test():
    _test()


def _test():
    neatest.run(warnings=neatest.Warnings.fail)


@app.command()
def test_pkg():
    with Package() as pkg:
        pkg.run_shell_code('img2texture --version')
        # running console_scripts defined in setup.py
        pkg.run_shell_code('img2texture --help')
        pkg.run_shell_code('img2texture', expected_return_code=2)

        # running img2texture/__main__.py
        pkg.run_shell_code('python -m img2texture',
                           expected_return_code=2)
        pkg.run_shell_code('python -m img2texture --help',
                           expected_return_code=0)
    print("\nPackage is OK!")


@app.command()
def run():
    subprocess.call([sys.executable, "-m", "img2texture"])


@app.command()
def lint():
    _lint()


def _lint():
    print("Running mypy...")
    if subprocess.call(['mypy', 'img2texture',
                        '--ignore-missing-imports']) != 0:
        exit(1)


def _replace_build_date(fn: Path):
    now = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
    text = fn.read_text()
    new_text = re.sub(
        r'__build_timestamp__.+',
        f'__build_timestamp__ = "{now}"',
        text)
    print(new_text)
    assert new_text != text, "timestamp not changed"
    fn.write_text(new_text)


def _get_single_file(dirpath: Path) -> Path:
    exes = list(dirpath.glob("*"))
    assert len(exes) == 1
    return Path(exes[0])


@app.command()
def build():
    name = "img2texture"
    project_dir = Path(__file__).parent

    _test()
    _lint()

    _replace_build_date(Path("img2texture/_constants.py"))

    compile.run([
        "--clean", "--onefile", "-y",
        "--collect-all", "img2texture",


        #"--log-level", "DEBUG",
        #"--specpath", "pyinstaller.myspec",
        "--exclude-module", 'FixTk',
        "--exclude-module", 'tcl',
        "--exclude-module", 'tk',
        "--exclude-module", '_tkinter',
        "--exclude-module", 'tkinter',
        "--exclude-module", 'Tkinter',
        "--exclude-module", "IPython",
        "--exclude-module", "mypy",
        "--exclude-module", "pip",
        "--exclude-module", "click",
        "--exclude-module", "neatest",
        "--exclude-module", "chkpkg",
        "--name", name, "_run.py"
    ])

    exe = _get_single_file(project_dir / "dist")
    print()
    print(f"Created {exe}")
    print(f"Exe size: {exe.stat().st_size / 1024 / 1024:.0f} MiB")

    os.remove(project_dir / "img2texture.spec")  # этот генерируется автоматичски
    shutil.rmtree(project_dir / "build")


if __name__ == "__main__":
    app()

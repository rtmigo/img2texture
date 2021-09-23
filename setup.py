from pathlib import Path

from setuptools import setup, find_packages


def load_module_dict(filename: str) -> dict:
    import importlib.util as ilu
    filename = Path(__file__).parent / filename
    spec = ilu.spec_from_file_location('', filename)
    module = ilu.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.__dict__


name = "img2texture"

readme = (Path(__file__).parent / 'README.md').read_text(encoding="utf-8")

setup(
    name=name,
    version="0.2.0",

    author="Artyom Galkin",
    author_email="ortemeo@gmail.com",
    url='https://github.com/rtmigo/img2texture_py',

    packages=find_packages(include=[name, f'{name}.*']),

    python_requires='>=3.7',
    install_requires=["pillow", "click"],

    long_description=readme,
    long_description_content_type='text/markdown',

    license="MIT",

    entry_points={
        'console_scripts': [
            'bman = blenderman:cli',
        ]},

    keywords="".split(),

    classifiers=[
        'License :: OSI Approved :: BSD License',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Environment :: Console",
        "Typing :: Typed",
        "Topic :: Software Development :: Build Tools",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows"
    ],

    test_suite="test_unit.suite"
)

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

constants = load_module_dict(f'{name}/_constants.py')

readme = (Path(__file__).parent / 'README.md').read_text(encoding="utf-8")
readme = "#"+readme.partition('\n#')[-1]

setup(
    name=name,
    version=constants['__version__'],

    author="Artёm iG",
    author_email="ortemeo@gmail.com",
    url='https://github.com/rtmigo/img2texture#readme',

    packages=find_packages(include=[name, f'{name}.*']),
    package_data={name: ["py.typed"]},

    python_requires='>=3.8, <4',  # 3.8 for Pillow 10
    install_requires=["pillow>=10.0.1"],  # fixing libwebp CVE-2023-4863

    description="Command line utility for converting images to seamless tiles.",
    long_description=readme,
    long_description_content_type='text/markdown',

    license=constants['__license__'],

    entry_points={
        'console_scripts': [
            'img2texture = img2texture:cli',
        ]},

    keywords="photo image texture tile seamless".split(),

    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Environment :: Console",
        "Typing :: Typed",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows"
    ],

    test_suite="test_unit.suite"
)
from chkpkg import Package

if __name__ == "__main__":
    with Package() as pkg:
        # running console_scripts defined in setup.py
        pkg.run_shell_code('img2texture --help')
        pkg.run_shell_code('img2texture', expected_return_code=2)

        # running img2texture/__main__.py
        pkg.run_shell_code('python -m img2texture',
                           expected_return_code=2)
        pkg.run_shell_code('python -m img2texture --help',
                           expected_return_code=0)

    print("\nPackage is OK!")

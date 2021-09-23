from chkpkg import Package

if __name__ == "__main__":
    with Package() as pkg:
        pkg.run_shell_code('img2texture --help')
        pkg.run_shell_code('img2texture', expected_return_code=2)

    print("\nPackage is OK!")

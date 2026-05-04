from functions.run_python_file import run_python_file

def main():
    print('Result for running "main.py":')
    print(run_python_file("calculator", "main.py"))

    print('\nResult for running "main.py" with args ["3 + 5"]:')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print('\nResult for running "tests.py":')
    print(run_python_file("calculator", "tests.py"))

    print('\nResult for running "../main.py":')
    print(run_python_file("calculator", "../main.py"))

    print('\nResult for running "nonexistent.py":')
    print(run_python_file("calculator", "nonexistent.py"))

    print('\nResult for running "lorem.txt":')
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
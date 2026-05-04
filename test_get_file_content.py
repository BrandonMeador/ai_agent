from config import MAX_CHARS
from functions.get_file_content import get_file_content

def main():
    lorem_result = get_file_content("calculator", "lorem.txt")

    print("Result for 'lorem.txt':")
    print(f"Length: {len(lorem_result)}")

    expected_truncation_message = (
        f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    )

    if expected_truncation_message in lorem_result:
        print("Truncation message found")
    else:
        print("Truncation message NOT found")

    print("\nResult for 'main.py':")
    print(get_file_content("calculator", "main.py"))

    print("\nResult for 'pkg/calculator.py':")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\nResult for '/bin/cat':")
    print(get_file_content("calculator", "/bin/cat"))

    print("\nResult for 'pkg/does_not_exist.py':")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()
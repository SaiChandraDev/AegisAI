
from collections import Counter
from pathlib import Path

LOG_FILE = Path(__file__).parent / "sample.log"


def find_errors(lines):
    errors = (
        line.strip()
        for line in lines
        if "ERROR" in line.upper()
    )
    return Counter(message for message in errors if message)


def main():
    with LOG_FILE.open("r", encoding="utf-8") as file:
        counts = find_errors(file)

    print("Error summary:")

    if not counts:
        print("No error messages found.")
        return

    for message, count in counts.most_common():
        print(f"{count}x - {message}")


if __name__ == "__main__":
    main()

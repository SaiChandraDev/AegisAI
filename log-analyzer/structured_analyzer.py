import re
from collections import Counter
from pathlib import Path

LOG_FILE = Path(__file__).parent / "sample.log"

LOG_PATTERN = re.compile(
    r"^(?:(?P<timestamp>\d{4}-\d{2}-\d{2}"
    r"[T ]\d{2}:\d{2}:\d{2})\s+)?"
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)"
    r"\s*:\s*(?P<message>.*)$",
    re.IGNORECASE,
)


def parse_log_line(line):
    """Parse a log line into timestamp, level, and message."""
    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    data = match.groupdict()
    data["level"] = data["level"].upper()
    data["message"] = data["message"].strip()

    return data


def analyze_logs(lines):
    """Parse log lines and count ERROR and CRITICAL messages."""
    parsed_logs = []

    for line in lines:
        parsed = parse_log_line(line)

        if parsed is not None:
            parsed_logs.append(parsed)

    error_counts = Counter(
        log["message"]
        for log in parsed_logs
        if log["level"] in {"ERROR", "CRITICAL"}
    )

    return parsed_logs, error_counts


def rank_errors(error_counts):
    """Rank errors from most frequent to least frequent."""
    return error_counts.most_common()


def extract_log_context(logs, error_index, window=2):
    """
    Return log entries surrounding a target error.

    Args:
        logs: List of parsed log entries.
        error_index: Index of the error in the list.
        window: Number of entries to include on each side.

    Returns:
        A list containing the surrounding entries and the error.

    Raises:
        TypeError: If the index or window is not an integer.
        ValueError: If the window is negative.
        IndexError: If the error index is out of range.
    """
    if not isinstance(error_index, int) or isinstance(error_index, bool):
        raise TypeError("error_index must be an integer")

    if not isinstance(window, int) or isinstance(window, bool):
        raise TypeError("window must be an integer")

    if window < 0:
        raise ValueError("window cannot be negative")

    if not 0 <= error_index < len(logs):
        raise IndexError("error_index is outside the logs list")

    start = max(0, error_index - window)
    end = min(len(logs), error_index + window + 1)

    return logs[start:end]


def main():
    with LOG_FILE.open("r", encoding="utf-8") as file:
        logs, error_counts = analyze_logs(file)

    print(f"Parsed log entries: {len(logs)}")
    print("Error priority summary:")

    ranked_errors = rank_errors(error_counts)

    if not ranked_errors:
        print("No errors found.")
        return

    for message, count in ranked_errors:
        print(f"{count}x - {message}")


if __name__ == "__main__":
    main()

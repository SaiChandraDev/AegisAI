
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

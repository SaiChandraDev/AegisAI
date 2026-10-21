
import unittest
from collections import Counter

from structured_analyzer import (
    parse_log_line,
    analyze_logs,
    rank_errors,
)


class TestStructuredAnalyzer(unittest.TestCase):

    def test_parses_timestamp_and_level(self):
        result = parse_log_line(
            "2026-10-20 10:30:45 ERROR: Database unavailable"
        )

        self.assertEqual(result["level"], "ERROR")
        self.assertEqual(
            result["timestamp"],
            "2026-10-20 10:30:45",
        )
        self.assertEqual(
            result["message"],
            "Database unavailable",
        )

    def test_parses_line_without_timestamp(self):
        result = parse_log_line("INFO: Application started")

        self.assertEqual(result["level"], "INFO")
        self.assertIsNone(result["timestamp"])
        self.assertEqual(result["message"], "Application started")

    def test_groups_repeated_errors(self):
        logs = [
            "ERROR: Database unavailable",
            "ERROR: Database unavailable",
            "CRITICAL: Service stopped",
            "INFO: Request received",
        ]

        parsed, counts = analyze_logs(logs)

        self.assertEqual(len(parsed), 4)
        self.assertEqual(counts["Database unavailable"], 2)
        self.assertEqual(counts["Service stopped"], 1)
        self.assertNotIn("Request received", counts)

    def test_ignores_unrecognized_lines(self):
        result = parse_log_line("This is not a standard log")

        self.assertIsNone(result)

    def test_ranks_errors_by_frequency(self):
        counts = Counter({
            "API timeout": 2,
            "Database unavailable": 5,
            "Service stopped": 1,
        })

        ranked = rank_errors(counts)

        self.assertEqual(
            ranked,
            [
                ("Database unavailable", 5),
                ("API timeout", 2),
                ("Service stopped", 1),
            ],
        )

    def test_handles_equal_error_counts(self):
        counts = Counter({
            "API timeout": 2,
            "Database unavailable": 2,
        })

        ranked = rank_errors(counts)

        self.assertEqual(len(ranked), 2)
        self.assertEqual(
            {count for _, count in ranked},
            {2},
        )


if __name__ == "__main__":
    unittest.main()

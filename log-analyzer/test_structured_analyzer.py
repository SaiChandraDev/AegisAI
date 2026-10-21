import unittest
from collections import Counter

from structured_analyzer import (
    parse_log_line,
    analyze_logs,
    rank_errors,
    extract_log_context,
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

    def test_extracts_context_before_and_after_error(self):
        raw_logs = [
            "INFO: Application started",
            "INFO: Database connection initializing",
            "WARNING: Database response is slow",
            "ERROR: Database connection failed",
            "INFO: Retry attempt started",
            "INFO: Retry attempt completed",
        ]

        logs, _ = analyze_logs(raw_logs)

        context = extract_log_context(
            logs,
            error_index=3,
            window=2,
        )

        self.assertEqual(
            [entry["message"] for entry in context],
            [
                "Database connection initializing",
                "Database response is slow",
                "Database connection failed",
                "Retry attempt started",
                "Retry attempt completed",
            ],
        )

    def test_extracts_context_at_start_of_logs(self):
        raw_logs = [
            "ERROR: Database unavailable",
            "INFO: Retry started",
            "INFO: Retry completed",
        ]

        logs, _ = analyze_logs(raw_logs)

        context = extract_log_context(
            logs,
            error_index=0,
            window=2,
        )

        self.assertEqual(len(context), 3)
        self.assertEqual(
            context[0]["message"],
            "Database unavailable",
        )

    def test_extracts_context_at_end_of_logs(self):
        raw_logs = [
            "INFO: Application started",
            "INFO: Request received",
            "ERROR: API timeout",
        ]

        logs, _ = analyze_logs(raw_logs)

        context = extract_log_context(
            logs,
            error_index=2,
            window=2,
        )

        self.assertEqual(len(context), 3)
        self.assertEqual(
            context[-1]["message"],
            "API timeout",
        )

    def test_extracts_error_only_when_window_is_zero(self):
        raw_logs = [
            "INFO: Application started",
            "ERROR: API timeout",
            "INFO: Retry started",
        ]

        logs, _ = analyze_logs(raw_logs)

        context = extract_log_context(
            logs,
            error_index=1,
            window=0,
        )

        self.assertEqual(len(context), 1)
        self.assertEqual(context[0]["message"], "API timeout")

    def test_rejects_negative_window(self):
        logs, _ = analyze_logs(["ERROR: API timeout"])

        with self.assertRaises(ValueError):
            extract_log_context(logs, error_index=0, window=-1)

    def test_rejects_out_of_range_index(self):
        logs, _ = analyze_logs(["ERROR: API timeout"])

        with self.assertRaises(IndexError):
            extract_log_context(logs, error_index=5)

    def test_rejects_non_integer_index(self):
        logs, _ = analyze_logs(["ERROR: API timeout"])

        with self.assertRaises(TypeError):
            extract_log_context(logs, error_index="0")


if __name__ == "__main__":
    unittest.main()

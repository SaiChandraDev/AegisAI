
import unittest
from structured_analyzer import parse_log_line, analyze_logs


class TestStructuredAnalyzer(unittest.TestCase):

    def test_parses_timestamp_and_level(self):
        result = parse_log_line(
            "2026-10-20 10:30:45 ERROR: Database unavailable"
        )

        self.assertEqual(result["level"], "ERROR")
        self.assertEqual(result["timestamp"], "2026-10-20 10:30:45")
        self.assertEqual(result["message"], "Database unavailable")

    def test_parses_line_without_timestamp(self):
        result = parse_log_line("INFO: Application started")

        self.assertEqual(result["level"], "INFO")
        self.assertIsNone(result["timestamp"])

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
        self.assertIsNone(parse_log_line("This is not a standard log"))


if __name__ == "__main__":
    unittest.main()

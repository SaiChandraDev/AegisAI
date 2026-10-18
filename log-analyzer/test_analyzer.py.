
import unittest
from analyzer import find_errors


class TestLogAnalyzer(unittest.TestCase):

    def test_counts_repeated_errors(self):
        logs = [
            "INFO: Application started",
            "ERROR: Database connection failed",
            "ERROR: Database connection failed",
            "ERROR: API timeout",
        ]

        result = find_errors(logs)

        self.assertEqual(
            result["ERROR: Database connection failed"], 2
        )
        self.assertEqual(result["ERROR: API timeout"], 1)

    def test_returns_empty_result_without_errors(self):
        logs = [
            "INFO: Application started",
            "INFO: Request completed",
        ]

        result = find_errors(logs)

        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()

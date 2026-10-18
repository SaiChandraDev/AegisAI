
# AegisAI 🛡️

An AI-powered incident investigation assistant, built step by step.

AegisAI aims to help software engineers investigate application incidents by analyzing logs, identifying repeated errors, and eventually suggesting possible causes and fixes for human review.

## Current Progress

### Log Analyzer
- Reads application log files
- Identifies error messages
- Counts repeated errors
- Includes unit tests for the core logic

## Project Structure

```text
AegisAI/
└── log-analyzer/
    ├── analyzer.py
    ├── sample.log
    └── test_analyzer.py
```

## Requirements

- Python 3.10 or later
- No external packages needed for the log analyzer

## Run the Analyzer

From the repository root:

```bash
python log-analyzer/analyzer.py
```

## Run the Tests

```bash
python -m unittest discover -s log-analyzer -p "test_*.py" -v
```

## Roadmap

- [x] Build the initial log analyzer
- [x] Add unit tests
- [ ] Verify execution and test results
- [ ] Add structured log analysis
- [ ] Build an API using FastAPI
- [ ] Integrate AI-assisted incident investigation
- [ ] Create a web dashboard

## Important

This project is under active development. Features will be added and verified incrementally.

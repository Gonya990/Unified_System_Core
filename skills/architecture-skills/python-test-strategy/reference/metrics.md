# Test Suite Metrics

## Runtime budgets
- Commit stage (unit + fast checks) < 5 min.
- Adapter pack < 5 min total, parallelizable.
- Acceptance suite < 20 min (stretch goal 10).

## Flake thresholds
- Any test failing >0.5% of runs is a P0 bug.
- Capture flaky test names in `logs/flaky_tests.log`; quarantined tests must reference issue IDs.

## Coverage expectations
- Unit + acceptance combined branch coverage ≥ previously reported value (see `coverage.xml`).
- Adapter tests must touch every SQL path, especially custom queries.

## Reporting loop
- After each CI run, update the dashboard script in `scripts/` if metrics regress.
- Document slow tests in PR summaries and link to work items.

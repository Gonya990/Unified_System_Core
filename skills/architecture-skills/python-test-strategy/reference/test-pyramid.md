# Test Pyramid Decision Aid

## Contents
- Classification questions
- Expected volume & runtime targets
- Escalation rules

## Classification questions
1. **Does the logic require real I/O?** If no → unit test.
2. **Are you verifying adapter code that touches DB/filesystem/HTTP?** → adapter test.
3. **Are you proving business capabilities via public API of a single service?** → acceptance test.
4. **Are multiple independently deployed services involved?** → stop; replace with contract tests or fakes.

## Volume & runtime targets
- **Unit**: thousands; each < 100 ms; total suite seconds.
- **Adapter**: handful per boundary; each < 2 s using Testcontainers or temporary files.
- **Acceptance**: per critical feature; whole suite < 20 min (ideal < 10) and runs every pipeline.

## Escalation rules
- If a unit test needs I/O, refactor to introduce a port.
- If adapter tests fail intermittently, add health checks to containers and retry logic in test setup, not production code.
- If acceptance tests exceed runtime budget, parallelize or trim scenarios—slow feedback violates Farley principles.

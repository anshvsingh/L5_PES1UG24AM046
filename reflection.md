# Lab 5: Reflection

**Name:** Ansh Vardhan Singh  **SRN:** PES1UG24AM046

> Note: the handout text I had did not list the four questions explicitly, so these use the standard Lab 5 reflection prompts. Replace the headings if your handout words them differently.

**1. Which tool did you find the most useful, and why?**
Each caught a different layer, but Pylint was the most useful overall. It found the most issues (bugs like the mutable default and the bare `except`, plus design smells such as the redefined outer name) and gave a numeric score that made progress visible (5.37 → 10.00). Bandit was the most important for *risk*: its two High findings (`os.system` shell injection and MD5) were the only things in the file that could directly hurt a real user. Flake8 was the quickest to clear but only covers style.

**2. Did any tool report something that was a false positive or not worth fixing? Did the tools miss anything?**
Some findings are context-dependent. For example, Bandit's MD5 finding would be a non-issue if MD5 were used only as a non-security checksum (it suggests `usedforsecurity=False` for that case), and the `random` warning would not matter for a game. Here a booking PIN is security-sensitive, so I fixed both. The tools also missed real problems: the hardcoded `BOX_OFFICE_SECRET_PASS_2026` that gets printed to the console (it is just a string to a linter), the `str(dict)` "seating chart", `cancel_seat` reporting success for a seat that doesn't exist, and `main()` running on import. Those needed reading the output and the code, not running tools.

**3. How would you integrate static analysis into a real development workflow?**
Run Flake8 and Pylint as a pre-commit hook so style and obvious bugs never reach the repo, and run all three in CI (e.g. GitHub Actions) on every pull request, failing the build on any Bandit High/Medium finding or a Pylint score below a threshold such as 9.0. Findings that are deliberately accepted get an inline suppression (`# nosec`, `# pylint: disable=`) with a written reason, so the exceptions are visible in review.

**4. What tangible improvements did you see in the code after the fixes?**
Security: no shell injection, no `eval`, no weak hash, no predictable PIN, no secret in source. Correctness: no state shared between calls, errors are reported instead of swallowed, and the file handle is always closed. Maintainability: PEP 8 naming, docstrings, no dead code, and an import-safe module with a `__main__` guard, so functions can now be unit tested without side effects. Score went from 5.37 to 10.00 with 0 Bandit and 0 Flake8 findings, and the program still produces the same demo output.

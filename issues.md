# Lab 5: Issues Found in `ticket_booking_system.py`

**Name:** Ansh Vardhan Singh  **SRN:** PES1UG24AM046

Line numbers refer to the **original** file. Sorted by severity.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built from input (`os.system`) | Security (Bandit B605, **High**) | 58 | `os.system("echo ... " + filename)` passes a user-controllable filename to a shell, allowing command injection (e.g. `a.txt; rm -rf ~`). It is also needless, since `print` does the same thing. | Removed `os.system`; use `print()`. |
| Weak MD5 hash | Security (Bandit B324, **High**) | 47 | MD5 is broken and collision-prone, so it should not be used to fingerprint tickets. | Switched to `hashlib.sha256`. |
| `eval()` on user-supplied promo string | Security (Bandit B307, **Medium**; Pylint W0123) | 42 | `eval(promo_expr)` executes arbitrary Python, so a promo string like `__import__('os').system(...)` runs code. It also allows nonsense prices (negative, or higher than base). The local `base_price` only exists for `eval`, which is why Pylint called it unused. | Replaced the expression with a numeric `discount_rate` (0.0 to 1.0), validated, and compute `price * (1 - rate)` directly. |
| Hardcoded secret and secret printed | Security / logic (not flagged by any tool) | 66, 76 | `BOX_OFFICE_SECRET_PASS_2026` is committed in source and then printed to the console. Credentials in code end up in git history and logs. | Read from `BOX_OFFICE_KEY` env var; print only whether it is configured. |
| Predictable PIN generator | Security (Bandit B311, Low) | 51 | `random.randint` is a Mersenne Twister PRNG; its output can be predicted, which is unsuitable for booking PINs. | Use `secrets.randbelow(9000) + 1000`. |
| Bare `except: pass` hiding errors | Bug / Security (Pylint W0702, Flake8 E722, Bandit B110) | 24-27 | Swallows every error, including `KeyError` for a bad seat ID and `KeyboardInterrupt`. Cancelling a non-existent seat silently "works". | Removed try/except; look up the seat with `.get()` and return `True`/`False` so callers know the outcome. |
| Mutable default argument | Bug (Pylint W0102) | 15 | `order_history=[]` is created once and shared across all calls. Here it is also useless, since the log is lost and the list grows forever. | Default to `None` and create a fresh list inside the function. |
| Resource leak: file opened without `with` | Bug / quality (Pylint R1732, W1514) | 55-57 | If `write` raises, `f.close()` never runs. No encoding is specified, so behaviour varies by OS. | `with open(filename, "w", encoding="utf-8")`. |
| `str(theater_seats)` as the "chart" | Logic (not flagged by any tool) | 56 | The exported "seating chart" is just a Python dict repr dumped on one line, not readable or parseable. | Write one line per seat: ID, tier, price, SOLD/FREE. |
| Unused import / variables | Quality (Pylint W0611, W0612; Flake8 F401, F841) | 6, 31, 63 | `math` is never used, `booking_fee` is dead code, and `seat` in the loop is unused. | Deleted them; replaced the loop with `sum(...)`. |
| Redefined outer name | Quality (Pylint W0621) | 61 | Parameter `theater_seats` shadows the global of the same name. | Renamed the parameter to `seats`. |
| Comparison to `None` with `==` | Style (Pylint C0121, Flake8 E711) | 32 | `== None` should use identity. | Use `is None` / `is not None`. |
| Needless if/else returning booleans | Quality (Pylint R1703, R1705) | 33-36 | Four lines to express a boolean. | `return seat is not None and not seat["is_sold"]`. |
| Non-snake_case function name | Style (Pylint C0103) | 15 | `reserveSeat` violates PEP 8 naming. | Renamed to `reserve_seat` (and updated the call in `main`). |
| `%` string formatting | Style (Pylint C0209) | 19 | Old-style formatting; line is also 82 chars (Flake8 E501). | Use an f-string; line is now under 79 chars. |
| Missing docstrings | Style (Pylint C0116) | 15 to 69 | Every function lacked a docstring. | Added a concise docstring to each function. |
| `main()` runs on import | Design (not flagged) | 82 | Importing the module immediately executes the demo and writes a file. | Wrapped in `if __name__ == "__main__":`. |
| Missing final newline | Style (Pylint C0304, Flake8 W292) | 82 | File does not end with a newline. | Added trailing newline. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.37 / 10 | **10.00 / 10** |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | **0 issues** |
| Flake8 | 7 warnings | **0 warnings** |

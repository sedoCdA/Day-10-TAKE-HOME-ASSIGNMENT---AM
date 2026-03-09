# log_analyzer.py
# Day 10 AM - Server Log Analyzer using Counter and defaultdict

from collections import Counter, defaultdict
import re

# -----------------------------------------
# Simulated Server Log
# -----------------------------------------
raw_logs = [
    "2026-03-06 08:01:12 INFO  auth       User login successful",
    "2026-03-06 08:02:45 ERROR db         Connection timeout",
    "2026-03-06 08:03:10 INFO  api        GET /products 200",
    "2026-03-06 08:04:33 WARNING auth     Invalid token received",
    "2026-03-06 08:05:01 ERROR db         Connection timeout",
    "2026-03-06 08:06:15 INFO  api        GET /orders 200",
    "2026-03-06 08:07:22 ERROR api        POST /checkout failed",
    "2026-03-06 08:08:45 INFO  auth       User login successful",
    "2026-03-06 08:09:13 CRITICAL db      Database unreachable",
    "2026-03-06 08:10:05 ERROR auth       Too many login attempts",
    "2026-03-06 08:11:30 INFO  api        GET /products 200",
    "2026-03-06 08:12:44 WARNING api      Rate limit approaching",
    "2026-03-06 08:13:55 ERROR db         Connection timeout",
    "2026-03-06 08:14:10 INFO  auth       User logout successful",
    "2026-03-06 08:15:22 ERROR api        POST /checkout failed",
    "2026-03-06 08:16:33 CRITICAL auth    Account locked out",
    "2026-03-06 08:17:45 INFO  db         Query executed in 12ms",
    "2026-03-06 08:18:01 WARNING db       Slow query detected",
    "2026-03-06 08:19:15 ERROR auth       Too many login attempts",
    "2026-03-06 08:20:30 INFO  api        GET /users 200",
]

# -----------------------------------------
# 1. Parse Log Lines into Dicts
# -----------------------------------------
def parse_log(line):
    """
    Parses a single log line into a structured dict.
    Returns None if the line does not match expected format.
    """
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+(\w+)\s+(.*)"
    match = re.match(pattern, line.strip())
    if not match:
        return None
    return {
        "timestamp": match.group(1),
        "level":     match.group(2),
        "module":    match.group(3),
        "message":   match.group(4).strip(),
    }

def parse_all_logs(logs):
    """Parses all log lines, skipping any malformed entries."""
    parsed = []
    for line in logs:
        entry = parse_log(line)
        if entry:
            parsed.append(entry)
    return parsed

# -----------------------------------------
# 2. Counter Analysis
# -----------------------------------------
def analyse_logs(parsed_logs):
    """
    Uses Counter to find:
    - Most common error messages
    - Most active modules
    - Distribution of log levels
    """
    error_messages = Counter(
        entry.get("message")
        for entry in parsed_logs
        if entry.get("level") in ("ERROR", "CRITICAL")
    )

    module_activity = Counter(
        entry.get("module")
        for entry in parsed_logs
    )

    level_distribution = Counter(
        entry.get("level")
        for entry in parsed_logs
    )

    return error_messages, module_activity, level_distribution

# -----------------------------------------
# 3. Group Errors by Module
# -----------------------------------------
def errors_by_module(parsed_logs):
    """
    Uses defaultdict(list) to group error messages by module.
    """
    grouped = defaultdict(list)
    for entry in parsed_logs:
        if entry.get("level") in ("ERROR", "CRITICAL"):
            grouped[entry.get("module")].append(entry.get("message"))
    return grouped

# -----------------------------------------
# 4. Summary Report
# -----------------------------------------
def generate_summary(parsed_logs):
    """
    Generates a summary dict with key analytics.
    """
    total = len(parsed_logs)
    if total == 0:
        return {"error": "No log entries found."}

    error_messages, module_activity, level_distribution = analyse_logs(parsed_logs)

    error_count = sum(
        count for level, count in level_distribution.items()
        if level in ("ERROR", "CRITICAL")
    )

    top_errors    = error_messages.most_common(3)
    busiest_module = module_activity.most_common(1)[0][0]

    return {
        "total_entries":      total,
        "error_rate":         round((error_count / total) * 100, 2),
        "level_distribution": dict(level_distribution),
        "top_errors":         top_errors,
        "busiest_module":     busiest_module,
    }

# -----------------------------------------
# Main
# -----------------------------------------
if __name__ == "__main__":

    parsed = parse_all_logs(raw_logs)

    print("=" * 55)
    print("SERVER LOG ANALYZER")
    print("=" * 55)

    print(f"\nTotal log entries parsed: {len(parsed)}")

    error_msgs, modules, levels = analyse_logs(parsed)

    print("\nLog Level Distribution:")
    for level, count in levels.most_common():
        print(f"   {level}: {count}")

    print("\nMost Active Modules:")
    for module, count in modules.most_common():
        print(f"   {module}: {count} entries")

    print("\nTop Error Messages:")
    for msg, count in error_msgs.most_common(3):
        print(f"   [{count}x] {msg}")

    print("\nErrors Grouped by Module:")
    for module, errors in errors_by_module(parsed).items():
        print(f"   {module}:")
        for e in errors:
            print(f"      - {e}")

    print("\nSummary Report:")
    summary = generate_summary(parsed)
    for key, value in summary.items():
        print(f"   {key}: {value}")

    # -----------------------------------------
    # Self-Study Note: Python logging module
    # -----------------------------------------
    """
    Python's logging module uses format strings like:
    '%(asctime)s %(levelname)s %(name)s %(message)s'

    To add logging to a real application:

        import logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(module)s %(message)s',
            filename='app.log'
        )
        logging.info("Application started")
        logging.error("Something went wrong")

    Levels in order of severity:
        DEBUG < INFO < WARNING < ERROR < CRITICAL
    """
```

---

### Step 3 — Commit Message
```
feat(day10): Part B - Server log analyzer using Counter and defaultdict

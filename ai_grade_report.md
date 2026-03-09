# AI-Augmented Task — Student Grade Report Analysis

---

## 1. Prompt Used

"Write a Python function that takes two dictionaries representing student
grades from two different semesters and produces a merged report showing:
combined GPA, grade trend (improving/declining/stable), and subjects common
to both semesters. Use defaultdict and dict comprehension."

---

## 2. AI-Generated Output
```python
from collections import defaultdict

def merge_grade_report(sem1, sem2):
    common_subjects = {k: (sem1[k], sem2[k]) for k in sem1 if k in sem2}
    combined_gpa = sum(sem2.values()) / len(sem2)
    trends = {}
    for subject in common_subjects:
        if sem2[subject] > sem1[subject]:
            trends[subject] = "improving"
        elif sem2[subject] < sem1[subject]:
            trends[subject] = "declining"
        else:
            trends[subject] = "stable"
    return {
        "common_subjects": common_subjects,
        "combined_gpa": combined_gpa,
        "trends": trends
    }
```

---

## 3. Critical Evaluation of AI Code

### Does it handle missing subjects?
Partially. It finds common subjects correctly using `if k in sem2`.
However it does not report subjects unique to each semester at all.

### Does it use .get() safely?
No. It uses `sem1[k]` and `sem2[k]` directly throughout.
If a key is missing for any reason this raises a KeyError.

### Is the trend calculation correct?
The per-subject trend logic is correct.
However the overall combined_gpa is wrong — it only averages sem2 grades,
completely ignoring sem1. A true combined GPA should average across both.

### Does it handle edge cases?
- Empty dicts: `sum(sem2.values()) / len(sem2)` raises ZeroDivisionError
- Single semester: no handling, crashes silently
- No type hints or docstrings provided

### Is the code Pythonic?
Partially. Dict comprehension is used for common_subjects which is good.
But the trends loop could also be a dict comprehension.

---

## 4. Improved Version
```python
from collections import defaultdict

def merge_grade_report(
    sem1: dict[str, float],
    sem2: dict[str, float]
) -> dict:
    """
    Merges two semester grade dicts into a combined report.

    Args:
        sem1: Subject -> grade mapping for semester 1
        sem2: Subject -> grade mapping for semester 2

    Returns:
        A dict containing:
        - common_subjects: subjects and grades in both semesters
        - only_in_sem1: subjects unique to semester 1
        - only_in_sem2: subjects unique to semester 2
        - combined_gpa: average across all grades in both semesters
        - trends: per-subject trend (improving/declining/stable)

    Edge cases handled:
        - Empty dicts
        - Single semester data
        - Missing keys use .get() safely
    """
    if not sem1 and not sem2:
        return {"error": "Both semesters are empty."}

    # Common subjects — safe access with .get()
    common_subjects = {
        subject: {
            "sem1": sem1.get(subject),
            "sem2": sem2.get(subject),
        }
        for subject in sem1
        if subject in sem2
    }

    # Subjects unique to each semester
    only_in_sem1 = {s: sem1[s] for s in sem1 if s not in sem2}
    only_in_sem2 = {s: sem2[s] for s in sem2 if s not in sem1}

    # Combined GPA across both semesters
    all_grades = list(sem1.values()) + list(sem2.values())
    combined_gpa = round(sum(all_grades) / len(all_grades), 2) if all_grades else 0.0

    # Per-subject trend using dict comprehension
    trends = {
        subject: (
            "improving" if sem2.get(subject, 0) > sem1.get(subject, 0)
            else "declining" if sem2.get(subject, 0) < sem1.get(subject, 0)
            else "stable"
        )
        for subject in common_subjects
    }

    return {
        "common_subjects": common_subjects,
        "only_in_sem1":    only_in_sem1,
        "only_in_sem2":    only_in_sem2,
        "combined_gpa":    combined_gpa,
        "trends":          trends,
    }


# Tests
sem1 = {"Math": 85, "Physics": 78, "English": 90, "Chemistry": 72}
sem2 = {"Math": 91, "Physics": 74, "English": 90, "Biology": 88}

report = merge_grade_report(sem1, sem2)

print("Common Subjects:", report["common_subjects"])
print("Only in Sem 1  :", report["only_in_sem1"])
print("Only in Sem 2  :", report["only_in_sem2"])
print("Combined GPA   :", report["combined_gpa"])
print("Trends         :", report["trends"])

# Edge case — empty dicts
print(merge_grade_report({}, {}))

# Edge case — one empty semester
print(merge_grade_report({"Math": 85}, {}))
```

---

## 5. Improvements Summary

| Issue                  | AI Code                          | Improved Version                        |
|------------------------|----------------------------------|-----------------------------------------|
| Safe key access        | Direct `d[key]` raises KeyError  | `.get()` used throughout                |
| Combined GPA           | Only averages sem2               | Averages across both semesters          |
| Empty dict crash       | ZeroDivisionError                | Handled with guard clause               |
| Missing subject report | Not included                     | only_in_sem1 and only_in_sem2 added     |
| Trend calculation      | Loop only                        | Replaced with dict comprehension        |
| Type hints             | None                             | Full type hints on function signature   |
| Docstring              | None                             | Google-style docstring with edge cases  |
```

---

### Step 3 — Commit Message
```
feat(day10): Part D - AI grade report analysis and improved solution

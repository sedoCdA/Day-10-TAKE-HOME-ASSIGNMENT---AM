# Interview Answers — Day 10 AM (Dictionaries)

---

## Q1 — Time Complexity of Dict Operations

### Lookup, Insert, Delete — Average Case: O(1)

Python dicts are implemented as hash tables.
When you do `d[key]`, Python:
1. Runs the key through a hash function → produces an integer index
2. Goes directly to that index in memory
3. Returns the value

This direct jump is why lookup, insert, and delete are all O(1) on average —
no scanning or sorting needed.

### Why worst case is O(n)

Hash collisions occur when two different keys produce the same hash index.
Python handles this using open addressing — it probes nearby slots to find
a free one. In an extreme case where many keys collide repeatedly, every
operation degrades to O(n) as Python scans through occupied slots.

In practice this is very rare. Python's hash function is designed to
distribute keys uniformly to minimise collisions.

### Hash function: strings vs integers

- Integers: hash(n) == n for most integers. Very fast, deterministic.
- Strings: Python applies the SipHash algorithm across all characters.
  The result depends on every character, so similar strings
  ("hello" vs "hellp") produce very different hashes.
- Note: hash values for strings are randomised per Python session
  (hash randomisation) to prevent denial-of-service attacks.

### Dict vs List — when to choose which

| Situation                              | Use       |
|----------------------------------------|-----------|
| Need fast lookup by a meaningful key   | dict      |
| Need to check membership frequently    | dict/set  |
| Need ordered sequence by position      | list      |
| Data has natural key-value structure   | dict      |
| Simple collection of items             | list      |
| Counting occurrences                   | Counter (dict subclass) |

---

## Q2 — Group Anagrams
```python
from collections import defaultdict

def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    """
    Groups a list of words by their anagram signature.
    Two words are anagrams if they contain the same characters.

    Approach:
        - Sort each word alphabetically to create a signature key
        - Use defaultdict(list) to collect words sharing the same key

    Example:
        'eat' -> sorted -> 'aet'
        'tea' -> sorted -> 'aet'  (same key, same group)

    Time complexity: O(n * k log k) where n = words, k = avg word length
    """
    groups = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)
    return dict(groups)

# Tests
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# {'aet': ['eat', 'tea', 'ate'], 'ant': ['tan', 'nat'], 'abt': ['bat']}

print(group_anagrams([]))
# {}

print(group_anagrams(["abc"]))
# {'abc': ['abc']}

print(group_anagrams(["ab", "ba", "cd", "dc"]))
# {'ab': ['ab', 'ba'], 'cd': ['cd', 'dc']}
```

---

## Q3 — Debug Problem

### Buggy code:
```python
def char_freq(text):
    freq = {}
    for char in text:
        freq[char] += 1          # Bug 1
    sorted_freq = sorted(freq, key=freq.get, reverse=True)
    return sorted_freq           # Bug 2
```

### Bug 1 — KeyError on first occurrence
`freq[char] += 1` assumes the key already exists in the dict.
On the first time a character is seen, it does not exist yet,
so Python raises a `KeyError`.

Fix: use `.get()` with a default of 0, or use `setdefault()`.
```python
freq[char] = freq.get(char, 0) + 1
```

### Bug 2 — Returns keys only, not (key, count) pairs
`sorted(freq, ...)` iterates over the dict's keys only.
The return value is a list of characters, with no counts attached.

Fix: sort `freq.items()` instead, which gives (character, count) tuples.
```python
sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
```

### Fully fixed function:
```python
def char_freq(text):
    """
    Returns list of (character, count) pairs sorted by frequency descending.
    """
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1          # Bug 1 fixed
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sorted_freq                               # Bug 2 fixed

# Tests
print(char_freq("hello"))
# [('l', 2), ('h', 1), ('e', 1), ('o', 1)]

print(char_freq("aabbcc"))
# [('a', 2), ('b', 2), ('c', 2)]

print(char_freq(""))
# []
```
```

---

### Step 3 — Commit Message
```
feat(day10): Part C - Interview answers (dict complexity, anagrams, debug fix)

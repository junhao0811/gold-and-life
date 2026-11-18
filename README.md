# 🏴‍☠️ Gold & Life: Pirate Raid Planner

A Python strategy simulation where you lead a crew of pirate adventurers raiding land sites guarded by defenders. Pick the right sites to maximise the gold you bring home, then do it again when rival crews are competing for the same loot. Every core data structure is **implemented from scratch**.

---

## ✨ Game modes

### Mode 1: Solo raid planner
Given a set of land sites (each with gold and guardians) and a crew size, decide where to send adventurers to **maximise total reward**.
- Sites are stored in a **binary search tree** keyed by their guardian-to-gold ratio
- An **in-order traversal** visits the most profitable sites first
- Sites can be updated on the fly (new gold, new guardians) in **O(log N)**

### Mode 2: Competing crews
Several crews raid the same sites over multiple days, each picking the best option available.
- Sites are ranked in a **max-heap** built **bottom-up in O(N)**
- Each crew takes the top site in **O(log N)**, and the site is re-scored and pushed back for the next crew
- A full day runs in **O(N + K log N)** for N sites and K crews

Every method is documented with its **best- and worst-case time complexity**.

---

## 🧱 Data structures built from scratch

`BinarySearchTree` · `MaxHeap` · `HashTable` · `Set` (array-based) · `LinkedStack` · `ReferentialArray` · merge sort · binary search

---

## 🚀 Run it

**Requires Python 3.10+.** No external packages.

```bash
python run_tests.py      # press Enter to run all tests
```

All tests pass.

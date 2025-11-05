# LLMHackathon

Benchmark coding LLMs on Project Euler–style problems under the **same machine**, **same time budget**, and **the same verification rules**.
Each model’s solution is executed in isolation, runtime is measured, correctness is verified against a ground truth, a **score** is computed (by difficulty & latency), and a **leaderboard** is printed.

---

## ✨ What this does

- Discovers problems in `Questions/<problem_id>/`.
- Runs each `*.py` solution (one per model) **in a fresh subprocess**.
- Measures wall-clock time (seconds).
- Verifies stdout against the expected single value.
- Applies scoring rules (difficulty points, per-minute late penalty, timeout = zero).
- Writes a detailed CSV (`results.csv`) and prints a **ranked leaderboard**.

---

## 🏆 Sample Results and Leaderboard

```text
📊 Test Results:
 112 | ChatGPT-5                 | 1.94       | ✅
 112 | Claude-Haiku-4.5          | 3.667      | ✅
 112 | DeepSeek-2025-10          | 0.112      | ❌ ()
 112 | Gemini-Flash-2.5-pro      | 1.797      | ✅
 145 | ChatGPT-5                 | 0.104      | ✅
 145 | Claude-Haiku-4.5          | 213.857    | ✅
 145 | DeepSeek-2025-10          | 0.489      | ❌ (227485267000992000)
 145 | Gemini-Flash-2.5-pro      | 184.367    | ✅
 172 | ChatGPT-5                 | 0.452      | ✅
 172 | Claude-Haiku-4.5          | 5.537      | ✅
 172 | DeepSeek-2025-10          | 0.104      | ❌ ()
 172 | Gemini-Flash-2.5-pro      | 0.102      | ✅
 187 | ChatGPT-5                 | 0.102      | ❌ ()
 187 | Claude-Haiku-4.5          | 44.596     | ✅
 187 | DeepSeek-2025-10          | 0.099      | ❌ ()
 187 | Gemini-Flash-2.5-pro      | 0.098      | ❌ ()
 190 | ChatGPT-5                 | 0.103      | ✅
 190 | Claude-Haiku-4.5          | 0.098      | ✅
 190 | DeepSeek-2025-10          | 0.096      | ✅
 190 | Gemini-Flash-2.5-pro      | 0.101      | ❌ ()
 206 | ChatGPT-5      _          | 0.1        | ❌ ()
 206 | Claude-Haiku-4.5          | 30.79      | ✅
 206 | DeepSeek-2025-10          | 0.142      | ❌ ()
 206 | Gemini-Flash-2.5-pro      | 2.076      | ❌ ()
 231 | ChatGPT-5                 | 1.261      | ✅
 231 | Claude-Haiku-4.5          | 3.873      | ❌ (5536738690946)
 231 | DeepSeek-2025-10          | 0.105      | ❌ ()
 231 | Gemini-Flash-2.5-pro      | 0.096      | ❌ ()
 301 | ChatGPT-5                 | 0.101      | ✅
 301 | Claude-Haiku-4.5          | 24.773     | ✅
 301 | DeepSeek-2025-10          | 0.12       | ✅
 301 | Gemini-Flash-2.5-pro      | 0.101      | ✅
 347 | ChatGPT-5                 | 7.442      | ✅
 347 | Claude-Haiku-4.5          | 4.619      | ✅
 347 | DeepSeek-2025-10          | 0.097      | ❌ ()
 347 | Gemini-Flash-2.5-pro      | 0.098      | ❌ ()
 357 | ChatGPT-5                 | 0.105      | ❌ ()
 357 | Claude-Haiku-4.5          | 0.102      | ❌ ()
 357 | DeepSeek-2025-10          | 0.104      | ❌ ()
 357 | Gemini-Flash-2.5-pro      | 0.098      | ❌ ()
 399 | ChatGPT-5                 | 0.098      | ❌ ()
 399 | Claude-Haiku-4.5          | timeout    | ❌ (Time Out)
 399 | DeepSeek-2025-10          | 0.114      | ❌ ()
 399 | Gemini-Flash-2.5-pro      | 7.412      | ❌ (9158128796692261,3.1e27328088)
 439 | ChatGPT-5                 | 164.1      | ❌ ()
 439 | Claude-Haiku-4.5        _ | timeout    | ❌ (Time Out)
 439 | DeepSeek-2025-10          | 2.169      | ❌ ()
 439 | Gemini-Flash-2.5-pro      | 1.234      | ❌ ()
 493 | ChatGPT-5                 | 0.646      | ❌ ()
 493 | Claude-Haiku-4.5          | 0.558      | ❌ ()
 493 | DeepSeek-2025-10          | 0.695      | ✅
 493 | Gemini-Flash-2.5-pro      | 0.664      | ✅
 502 | ChatGPT-5                 | 0.777      | ❌ ()
 502 | Claude-Haiku-4.5          | 188.115    | ❌ (Test cases:
F(4, 2) = 10 (expected: 10)
F(13, 10) = 3729050610636 (expected: 3729050610636)
F(10, 13) = 37959702514 (expected: 37959702514)

For the final answer: F(10^12, 100) + F(100000, 100000) + F(100, 10^12)
requires mathematical algorithms for large w values beyond bitmask DP.

The problem requires advanced techniques such as:
- Shape-based configuration enumeration
- Generating functions for configuration counting
- Mathematical optimization for specific problem structure)
 502 | DeepSeek-2025-10          | 0.669      | ❌ (21569431)
 502 | Gemini-Flash-2.5-pro      | 0.697      | ❌ (525741794)
 505 | ChatGPT-5                 | timeout    | ❌ (Time Out)
 505 | Claude-Haiku-4.5          | timeout    | ❌ (Time Out)
 505 | DeepSeek-2025-10          | 1.119      | ❌ ()
 505 | Gemini-Flash-2.5-pro      | 0.722      | ❌ (944972997119722000)
  54 | ChatGPT-5                 | 0.741      | ❌ ()
  54 | Claude-Haiku-4.5          | 1.267      | ❌ ()
  54 | DeepSeek-2025-10          | 1.264      | ❌ ()
  54 | Gemini-Flash-2.5-pro      | 0.677      | ❌ ()
  74 | ChatGPT-5                 | 8.752      | ✅
  74 | Claude-Haiku-4.5          | 12.127     | ✅
  74 | DeepSeek-2025-10          | 0.578      | ❌ ()
  74 | Gemini-Flash-2.5-pro      | 10.472     | ✅
  81 | ChatGPT-5                 | 0.65       | ❌ ()
  81 | Claude-Haiku-4.5          | 0.9        | ✅
  81 | DeepSeek-2025-10        t | 0.869      | ❌ ()
  81 | Gemini-Flash-2.5-pro      | 0.533      | ❌ ()
  92 | ChatGPT-5                 | timeout    | ❌ (Time Out)
  92 | Claude-Haiku-4.5          | 48.131     | ✅
  92 | DeepSeek-2025-10          | 0.75       | ❌ ()
  92 | Gemini-Flash-2.5-pro      | 4.596      | ✅
  99 | ChatGPT-5                 | 0.714      | ❌ ()
  99 | Claude-Haiku-4.5          | 0.705      | ❌ ()
  99 | DeepSeek-2025-10          | 0.709    s | ❌ ()
  99 | Gemini-Flash-2.5-pro      | 0.697      | ❌ ()

🏆 LLM Score Order (Weighted by difficulty):
 1. Claude-Haiku-4.5          405.00 pts
 2. ChatGPT-5                 323.75 pts
 3. Gemini-Flash-2.5-pro      221.25 pts
 4. DeepSeek-2025-10          138.75 pts

🏁 LLM Score Order (All questions equal — 100 pts each):
Text
 1. Claude-Haiku-4.5          1070.00 pts
 2. ChatGPT-5                 800.00 pts
 3. Gemini-Flash-2.5-pro      670.00 pts
 4. DeepSeek-2025-10          300.00 pts

---
```

## 📁 Repository layout

```text
LLMHackathon/
├── runner.py               # main runner (executes, verifies, scores, ranks)
├── Questions/                # problems live here (directory per problem id)
│   ├── 54/
│   │   ├── GPT-5.py
│   │   └── Claude-Haiku-4.5.py
│   ├── 81/
│   │   └── SomeModel.py
│   └── ...
└── README.md
```

> **Note:** The directory name is `Questions` .  
> You can change it in `runner.py` by editing `Questions Directory`.

---

## 🔧 Requirements

- Python **3.10+** (tested with Python 3.11)
- Same machine for all runs (so timing is comparable)
- Model solutions must print **only** the final answer via `print(...)`
- No interactive input; no network access
- Standard library only (no third-party packages)

---

## 🚀 Quick start

1. Put model solutions under `Questions/<problem_id>/<ModelName>.py`.

   Example:
   ```text
   Questions/54/GPT-5.py
   Questions/54/Claude-Haiku-4.5.py
   ```

2. Ensure each script prints **one single line** with the final numeric answer:
   ```python
   Questions/54/GPT-5.py
   Questions/54/Claude-Haiku-4.5.py
   # ... your computation ...
   print(376)
   ```

3. Update `EXPECTED_OUTPUTS` in `runner.py` with the expected `(answer, difficulty)`:
   ```python
   EXPECTED_OUTPUTS = {
       "54":  ("376", 10),
       "81":  ("427337", 10),
       "99":  ("709", 10),
       # ...
   }
   ```

4. Run:
   ```bash
   python3 runner.py
   ```

5. Inspect:
   - Console table (per-run results + leaderboard)
   - `results.csv` for archival & post-analysis

---

## 🧮 Scoring rules

- Each problem has a **difficulty score** (e.g., 10, 25, 70, …).
- If the model prints the **correct** answer **within 60 seconds** → **full difficulty points**.
- If the answer is correct but takes **longer than 60 seconds**, subtract **10 points per extra full minute**:
  - 61–120 s → −10
  - 121–180 s → −20
  - …
  - The minimum is **0 points** (no negative scores).
- If the answer is **wrong**, **timeout**, or **error** → **0 points**.
- Final **leaderboard** = sum of points across all problems, highest to lowest.

> `runner.py` uses `TIMEOUT = 600` seconds for execution safety.  
> The 60 s rule above applies to scoring (full points if `≤ 60 s`, otherwise per-minute penalties).

---

## 📄 CSV schema (`results.csv`)

Each row = one run of `<problem_id>/<model>.py`.

| Column               | Meaning                                  |
|----------------------|-------------------------------------------|
| `Question No`        | Problem id (e.g., `54`)                   |
| `LLM`                | Model name (derived from filename)        |
| `Execution Time (s)` | Runtime in seconds, or `timeout` / `hata` |
| `Is Correct    `     | `✅` for correct, `❌ (…reason…)` otherwise |

At the end of a run, the script:
- writes the CSV,
- re-reads it,
- computes scores,
- prints the **leaderboard** sorted from highest to lowest.

---

## 🧠 Prompt template (English)

Use a disciplined prompt so models produce *computational* code rather than hard-coded answers:

```text
In the attached image, you are given an algorithmic problem in the style of Project Euler.

This is a hackathon challenge. Your code will be executed in an independent evaluation system, and only the value printed via print(...) will be compared with the actual correct answer.

Your code is expected to compute the answer by itself by solving the given problem.

The execution environment provides the following resources:
	•	A 16-core multi-processor CPU
	•	64 GB of RAM
	•	An NVIDIA GPU with 8 GB of VRAM
	•	A Linux environment with Python 3.11 installed
	•	You may use NumPy, multiprocessing, and other standard Python libraries
	•	You may not use third-party libraries (e.g., sympy, numba, gmpy2, tensorflow)

Please:
	1.	Analyze the problem and choose an appropriate algorithm.
	2.	Consider using parallel processing (e.g., multiprocessing) or efficient memory handling to speed up computation.
	3.	Use fast numerical libraries like numpy when necessary.
	4.	Write Python 3 code that runs correctly and outputs only the final result using print(...).
	5.	Do not hardcode the answer in your code; compute it programmatically.
	6.	Use print(...) only for the final result — no debug or intermediate outputs.
	7.	The code must finish execution within 60 seconds and produce the correct result.

Notes:
	•	You are encouraged to utilize multi-core capabilities using tools such as multiprocessing.Pool or concurrent.futures.ProcessPoolExecutor.
	•	GPU acceleration may indirectly help via NumPy, but direct CUDA programming is not allowed.
	•	Please do not calculate or provide the final answer yourself — just write the code that computes it.
```

---

## ⚠️ Notes & tips

- **Floating answers** (e.g., Euler #493)  
  The judge uses **string equality**. If a problem expects a decimal string, print that exact string (e.g., `6.818741802`).  
  If you prefer tolerance-based checking, extend `runner.py` accordingly.

- **Parallelism**  
  Solutions may leverage `multiprocessing` to use multiple cores. Each solution runs in a **separate process**, so memory leaks don’t accumulate across runs.

- **Determinism**  
  Scripts must not depend on randomness unless they seed and deterministically converge to the **exact** expected value.

---

## ➕ Adding new problems

1. Create a folder: `Questions/<problem_id>/`
2. Add one or more model files: `*.py`
3. Add the expected `(answer, difficulty)` to `EXPECTED_OUTPUTS` in `runner.py`
4. Run `python3 runner.py`

---

## 🤝 Contributing

- Submit PRs that:
  - Add new problems/folders
  - Add new model baselines
  - Improve scoring/verification
  - Document best prompts for fair comparison

Please keep solutions free of external dependencies (standard library only).

---

## 🪪 License

GNU GENERAL PUBLIC LICENSE

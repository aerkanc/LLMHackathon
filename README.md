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

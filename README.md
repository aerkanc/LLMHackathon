# LLMHackathon

Benchmark coding LLMs on Project Euler–style problems under the **same machine**, **same time budget**, and **the same verification rules**.  
Each model’s solution is executed in isolation, runtime is measured, correctness is verified against a ground truth, a **score** is computed (by difficulty & latency), and a **leaderboard** is printed.

---

## ✨ What this does

- Discovers problems in `Sorular/<problem_id>/`.
- Runs each `*.py` solution (one per model) **in a fresh subprocess**.
- Measures wall-clock time (seconds).
- Verifies stdout against the expected single value.
- Applies scoring rules (difficulty points, per-minute late penalty, timeout = zero).
- Writes a detailed CSV (`sonuclar.csv`) and prints a **ranked leaderboard**.

---

## 📁 Repository layout

```text
LLMHackathon/
├── runner.py               # main runner (executes, verifies, scores, ranks)
├── Sorular/                # problems live here (directory per problem id)
│   ├── 54/
│   │   ├── GPT-4o.py
│   │   └── Claude-3.5.py
│   ├── 81/
│   │   └── SomeModel.py
│   └── ...
└── README.md
```

> **Note:** The directory name is `Sorular` (Turkish for *questions*).  
> You can change it in `runner.py` by editing `SORU_KLASORU`.

---

## 🔧 Requirements

- Python **3.10+** (tested with Python 3.11)
- Same machine for all runs (so timing is comparable)
- Model solutions must print **only** the final answer via `print(...)`
- No interactive input; no network access
- Standard library only (no third-party packages)

---

## 🚀 Quick start

1. Put model solutions under `Sorular/<problem_id>/<ModelName>.py`.

   Example:
   ```text
   Sorular/54/GPT-4o.py
   Sorular/54/Claude-3.5.py
   ```

2. Ensure each script prints **one single line** with the final numeric answer:
   ```python
   # Sorular/54/GPT-4o.py
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
   - `sonuclar.csv` for archival & post-analysis

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

## 📄 CSV schema (`sonuclar.csv`)

Each row = one run of `<problem_id>/<model>.py`.

| Column               | Meaning                                  |
|----------------------|-------------------------------------------|
| `Soru No`            | Problem id (e.g., `54`)                   |
| `LLM`                | Model name (derived from filename)        |
| `Çalışma Süresi (s)` | Runtime in seconds, or `timeout` / `hata` |
| `Çıktı Doğru mu`     | `✅` for correct, `❌ (…reason…)` otherwise |

At the end of a run, the script:
- writes the CSV,
- re-reads it,
- computes scores,
- prints the **leaderboard** sorted from highest to lowest.

---

## 🧠 Prompt template (English)

Use a disciplined prompt so models produce *computational* code rather than hard-coded answers:

```text
You will solve a Project Euler–style problem in a hackathon setting.

Rules:
1) Write Python 3 code that COMPUTES the answer and prints it via `print(...)`.
2) Do NOT hard-code the final number; your code must derive it.
3) No debug prints. Only a single final `print(...)`.
4) The code will run on a Linux machine with 16 CPU cores and 64 GB RAM (and an 8 GB NVIDIA GPU, no custom CUDA).
5) Standard library is allowed; third-party packages are not.
6) The judge will run your code and compare stdout with the ground truth.
7) Your solution must finish within 60 seconds for full credit.

Problem:
"""
[INSERT PROBLEM STATEMENT HERE]
"""
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

1. Create a folder: `Sorular/<problem_id>/`
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

MIT (or your preferred OSS license).

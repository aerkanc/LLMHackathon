# Project Agents Guide

## Project Intent

This repository benchmarks code-writing LLMs on Project Euler-style problems under equal conditions:

- same problem statement
- same machine
- same time budget
- same verification rules
- same scoring rules

Preserve that apples-to-apples comparison. Avoid changes that would quietly favor one model, one version, or one question format.

## Repository Map

- `runner.py`: benchmark runner. Executes `Questions/<id>/*.py`, measures runtime, checks exact stdout, writes `results.csv`, and prints leaderboards.
- `Questions/<id>/`: one folder per problem.
- `Questions/<id>/<id>.png`: the problem image shown to models.
- `Questions/<id>/*.py`: one solution file per model/version.
- `Questions/<id>/*.{txt,csv,...}`: optional local data files needed by a solution.
- `create-empty-answer-files.sh`: creates starter files for the current baseline model set.
- `requirements.txt`: currently only `numpy`.
- `results.csv`: generated artifact. Do not hand-edit unless the user explicitly asks for that.

## Benchmark Rules To Preserve

- Solutions must compute the answer programmatically. Do not hardcode known Euler answers or copy the value from `EXPECTED_OUTPUTS`.
- A solution script must print exactly one final answer via `print(...)`.
- No debug output, logging, prompts, or interactive input.
- Target runtime is `<= 60` seconds for full points.
- Hard execution timeout is `600` seconds in `runner.py`.
- Correctness is exact string equality against `EXPECTED_OUTPUTS`.
- Floating-point answers must match the expected string exactly.
- Wrong answers, errors, and timeouts score `0`.
- Scores are tracked in two modes:
  - difficulty-weighted
  - equal-points-per-question

Important: the current scoring code applies a `10` point penalty for each additional started minute after 60 seconds:

- `61-120s`: `-10`
- `121-180s`: `-20`
- etc.

## Working On Solution Files

When asked to add or improve a model answer:

1. Read the problem statement first. Use the image and any sibling data files.
2. Derive an algorithm that computes the answer; do not turn the benchmark into answer transcription.
3. Keep the script standalone inside that model's file unless the user explicitly asks for shared infrastructure.
4. Prefer the standard library. `numpy` and multiprocessing are acceptable when they materially help.
5. Do not add new third-party dependencies unless explicitly requested.
6. If a solution reads local input files, resolve them relative to the script file, not the process working directory.

Preferred pattern for local files:

```python
from pathlib import Path

DATA_FILE = Path(__file__).with_name("0054_poker.txt")
```

## Adding New Questions

When asked to add a new benchmark problem:

1. Create `Questions/<id>/`.
2. Add the problem image as `Questions/<id>/<id>.png`.
3. Add any auxiliary input files into the same folder.
4. Add the expected answer and difficulty weight to `EXPECTED_OUTPUTS` in `runner.py`.
5. Add or generate the per-model solution files.
6. Keep file names consistent with the model/version naming already used in the repo.

Do not assume there is only one active model set. This repository currently contains multiple generations of model/version names, for example:

- `ChatGPT-5`
- `ChatGPT-5.4`
- `Claude-Haiku-4.5`
- `Claude-Opus-4.6`
- `Gemini-Flash-2.5-pro`
- `Gemini-3.1-Pro`
- `DeepSeek-2025-10`
- `DeepSeek-V3.2`

Inspect the tree before automating file creation or cleanup.

## Canonical Prompt Context

The repo exists to compare code generated from the same Project Euler-style prompt. The important constraints from that benchmark prompt are:

- the model sees the problem as an image
- it must solve the problem itself
- only the final `print(...)` output is judged
- algorithm choice matters
- parallelism and memory efficiency are allowed when useful
- no hardcoded final answer
- no extra output

Historically, the benchmark has been framed around paid model variants and thinking/reasoning modes. The repository stores the resulting code, not the remote model settings, so do not claim those settings can be verified from the code alone.

## Verification Expectations

After touching benchmark logic or solution files:

- run the changed script directly when practical
- run `python3 runner.py` when practical
- if you do not run the full benchmark, say so clearly

If you change scoring, folder conventions, or setup instructions, keep `README.md` and `runner.py` aligned.

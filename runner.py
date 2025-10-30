import os
import time
import subprocess
import csv
import math
from pathlib import Path
from collections import defaultdict

QUESTION_DIR = "Questions"
RESULT_CSV = "results.csv"

EXPECTED_OUTPUTS = {
    "54":  ("376", 27.5),
    "74":  ("402", 15),
    "81":  ("427337", 37.5),
    "92":  ("8581146", 25),
    "99":  ("709", 17.5),
    "112": ("1587000", 20),
    "145": ("608720", 35),
    "172": ("227485267000992000", 71.25),
    "187": ("17427258", 55),
    "190": ("371048281", 53.75),
    "206": ("1389019170", 38.75),
    "231": ("7526965179680", 45),
    "301": ("2178309", 27.5),
    "347": ("11109800204052", 56.25),
    "357": ("1739023853137", 57.5),
    "399": ("1508395636674243,6.5e27330467", 80),
    "439": ("968697378", 97.5),
    "493": ("6.818741802", 57.5),
    "502": ("749485217", 98.75),
    "505": ("714591308667615832", 88.75),
}

TIMEOUT = 600  # 10 minutes
EQUAL_POINT = 100  # eşit ağırlıklı puan

def run_code(filepath, expected_output):
    try:
        start_time = time.time()
        result = subprocess.run(
            ["python3", filepath],
            capture_output=True,
            text=True,
            timeout=TIMEOUT
        )
        end_time = time.time()
        sure = round(end_time - start_time, 3)
        output = result.stdout.strip()
        success = output == expected_output
        return sure, output, success
    except subprocess.TimeoutExpired:
        return "timeout", "Time Out", False
    except Exception as e:
        # Normalize to a clear marker
        return "error", str(e), False

def export_result_csv(table):
    with open(RESULT_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=table[0].keys())
        writer.writeheader()
        writer.writerows(table)

def _score_for_time(base_point, exec_time):
    """
    60 sn'ye kadar ceza yok.
    60 sn üzeri her TAM dakika için 10 puan ceza (ceil ile yukarı yuvarlanır).
    Alt sınır 0.
    """
    if isinstance(exec_time, str):
        # timeout / error
        return 0.0
    t = float(exec_time)
    if t <= 60:
        return float(base_point)
    penalty = math.ceil((t - 60) / 60) * 10
    return max(0.0, float(base_point) - penalty)

def calculate_scores(csv_path):
    """
    İki ayrı toplam döndürür:
      - weighted_points: EXPECTED_OUTPUTS'deki zorluk puanlarına göre
      - equal_points: her soru 100 puan kabul edilirse
    Geri dönüş: (weighted_sorted, equal_sorted)
    """
    weighted_points = defaultdict(float)
    equal_points = defaultdict(float)

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question = row["Question No"]
            llm = row["LLM"]
            sure_raw = row["Execution Time (s)"]
            is_correct = row["Is Correct"].startswith("✅")

            # Normalize execution time field
            if isinstance(sure_raw, str):
                sr = sure_raw.strip().lower()
                if sr in ("timeout", "time out"):
                    exec_time = "timeout"
                elif sr in ("error",):
                    exec_time = "error"
                else:
                    # try parse float if possible
                    try:
                        exec_time = float(sure_raw)
                    except:
                        exec_time = "error"
            else:
                exec_time = float(sure_raw)

            expected_tuple = EXPECTED_OUTPUTS.get(question)
            if not expected_tuple:
                # soruya puan tablomuz yoksa bu soruyu skorlamadan geç
                continue

            expected_output, difficulty_point = expected_tuple

            if not is_correct:
                # yanlışsa her iki tabloda da puan 0
                continue

            # Doğruysa puan hesapla
            weighted_points[llm] += _score_for_time(difficulty_point, exec_time)
            equal_points[llm] += _score_for_time(EQUAL_POINT, exec_time)

    weighted_sorted = sorted(weighted_points.items(), key=lambda x: x[1], reverse=True)
    equal_sorted = sorted(equal_points.items(), key=lambda x: x[1], reverse=True)
    return weighted_sorted, equal_sorted

def main():
    table = []
    for question_path in sorted(Path(QUESTION_DIR).iterdir()):
        if question_path.is_dir():
            question_number = question_path.name
            expected_data = EXPECTED_OUTPUTS.get(question_number)
            if not expected_data:
                continue
            expected_output = expected_data[0]
            for py_file in sorted(question_path.glob("*.py")):
                llm_name = py_file.stem
                print(f"🚀 Running: {question_number} / {llm_name}")
                sure, response, correction = run_code(str(py_file), expected_output)
                table.append({
                    "Question No": question_number,
                    "LLM": llm_name,
                    "Execution Time (s)": sure,
                    "Is Correct": "✅" if correction else f"❌ ({response})"
                })

    if not table:
        print("No results found.")
        return

    export_result_csv(table)

    print("\n📊 Test Results:")
    for row in table:
        print(f"{row['Question No']:>4} | {row['LLM']:<25} | {row['Execution Time (s)']:<10} | {row['Is Correct']}")

    print("\n🏆 LLM Score Order (Weighted by difficulty):")
    weighted, equal = calculate_scores(RESULT_CSV)
    for order, (llm, point) in enumerate(weighted, 1):
        print(f"{order:>2}. {llm:<25} {point:.2f} pts")

    print("\n🏁 LLM Score Order (All questions equal — 100 pts each):")
    for order, (llm, point) in enumerate(equal, 1):
        print(f"{order:>2}. {llm:<25} {point:.2f} pts")

if __name__ == "__main__":
    main()

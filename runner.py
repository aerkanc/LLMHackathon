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
    "54":  ("376", 10),
    "81":  ("427337", 10),
    "99":  ("709", 10),
    "74":  ("402", 15),
    "92":  ("8581146", 15),
    "145": ("608720", 15),
    "112": ("1587000", 25),
    "190": ("17427258", 30),
    "206": ("1389019170", 40),
    "172": ("227485267000992000", 55),
    "231": ("7526965179680", 60),
    "357": ("1739023853137", 65),
    "301": ("2178309", 70),
    "493": ("6.818741802", 85),
    "505": ("302980501465712", 95),
    "439": ("968697378", 100),
}

TIMEOUT = 600  # 10 minutes

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
        return "Error", str(e), False

def export_result_csv(table):
    with open(RESULT_CSV, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=table[0].keys())
        writer.writeheader()
        writer.writerows(table)

def calculate_scores(csv_path):
    points = defaultdict(float)
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question = row["Question No"]
            llm = row["LLM"]
            sure = row["Execution Time (s)"]
            correction = row["Is Correct"].startswith("✅")
            expected_output, difficulty_point = EXPECTED_OUTPUTS.get(question, ("", 0))

            if correction:
                if isinstance(sure, str) and (sure == "timeout" or sure == "error"):
                    scor = 0
                else:
                    sure = float(sure)
                    if sure <= 60:
                        scor = difficulty_point
                    else:
                        penalty = math.ceil((sure - 60) / 60) * 10
                        scor = max(0, difficulty_point - penalty)
            else:
                scor = 0

            points[llm] += scor

    return sorted(points.items(), key=lambda x: x[1], reverse=True)

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
        print("No any results found.")
        return

    export_result_csv(table)

    print("\n📊 Test Results:")
    for row in table:
        print(f"{row['Question No']:>4} | {row['LLM']:<15} | {row['Execution Time (s)']:<10} | {row['Is Correct']}")

    print("\n🏆 LLM scor Order:")
    ordered_point = calculate_scores(RESULT_CSV)
    for order, (llm, point) in enumerate(ordered_point, 1):
        print(f"{order:>2}. {llm:<15} {point:.2f} point")

if __name__ == "__main__":
    main()

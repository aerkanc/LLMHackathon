#!/usr/bin/env bash
# create_model_files.sh
# Usage:
#   ./create_model_files.sh                 # Default: ./Questions
#   ./create_model_files.sh /path/to/Questions

set -euo pipefail

BASE_DIR="${1:-Questions}"

if [[ ! -d "$BASE_DIR" ]]; then
  echo "Hata: '$BASE_DIR' directory not founded." >&2
  exit 1
fi

declare -a FILES=(
  "Gemini-3.1-Pro.py"
  "Claude-Opus-4.6.py"
  "ChatGPT-5.4.py"
  "DeepSeek-V3.2.py"
)

# Default template for Python files
make_template() {
  local model_name="$1"
  cat <<'PYT'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def solve():
    # TODO: Implement the solution for this model variant
    # Print only the final answer as required by the judge
    pass

if __name__ == "__main__":
    solve()
PYT
}

shopt -s nullglob
for dir in "$BASE_DIR"/*/; do
  name="$(basename "$dir")"
  # Target is only numbered files
  if [[ "$name" =~ ^[0-9]+$ ]]; then
    for f in "${FILES[@]}"; do
      target="$dir$f"
      if [[ -e "$target" ]]; then
        # if exists don't touch
        continue
      fi
      # create file and inject content
      make_template "$f" > "$target"
      chmod +x "$target"
      echo "Oluşturuldu: $target"
    done
  fi
done

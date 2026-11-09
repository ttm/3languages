#!/usr/bin/env bash
# Reproducible Markdown -> typeset academic PDF build.
# Requires pandoc and XeLaTeX (texlive-xetex); source is always paper.md.
set -euo pipefail

cd "$(dirname "$0")/.."
command -v pandoc >/dev/null || { echo "pandoc is required" >&2; exit 1; }
command -v xelatex >/dev/null || { echo "xelatex is required" >&2; exit 1; }

pandoc paper.md \
  --from=markdown+tex_math_dollars+pipe_tables+smart \
  --standalone \
  --pdf-engine=xelatex \
  --output=paper.pdf \
  --metadata=lang:en \
  --variable=papersize:a4 \
  --variable=geometry:top=25mm \
  --variable=geometry:bottom=25mm \
  --variable=geometry:left=26mm \
  --variable=geometry:right=26mm \
  --variable=mainfont:"DejaVu Serif" \
  --variable=sansfont:"DejaVu Sans" \
  --variable=monofont:"DejaVu Sans Mono" \
  --variable=fontsize:11pt \
  --variable=linestretch:1.13 \
  --variable=colorlinks:true \
  --variable=urlcolor:blue \
  --variable=linkcolor:blue

# Both production checks prevent silently committing an empty or image-only PDF.
test -s paper.pdf
if command -v pdfinfo >/dev/null; then pdfinfo paper.pdf | grep -E "^Pages:[[:space:]]+[1-9]"; fi
if command -v pdftotext >/dev/null; then
  pdftotext paper.pdf paper.pdf.txt
  grep -Fq "From Three Languages to Epistemic" paper.pdf.txt
  grep -Fq "References" paper.pdf.txt
  rm -f paper.pdf.txt
fi
echo "Built paper.pdf ($(wc -c < paper.pdf) bytes)"

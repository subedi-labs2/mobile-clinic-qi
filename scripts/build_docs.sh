#!/usr/bin/env bash
# Build Word (.docx) and PDF versions of the Phase 1 documents into dist/.
# Requires: pandoc. PDF also requires: weasyprint (pip install weasyprint).
set -euo pipefail
cd "$(dirname "$0")/.."

OUT=dist
mkdir -p "$OUT"
CSS=scripts/print.css

sources=(docs/*.md data/data-dictionary.md templates/screening-form.md templates/pdsa-worksheet.md)

have_pdf=1
command -v weasyprint >/dev/null 2>&1 || python3 -c "import weasyprint" 2>/dev/null || have_pdf=0
[[ $have_pdf -eq 0 ]] && echo "weasyprint not found: skipping PDFs (pip install weasyprint)" >&2

to_pdf() {  # $1 = html in, $2 = pdf out
  if command -v weasyprint >/dev/null 2>&1; then weasyprint -q "$1" "$2"
  else python3 -m weasyprint -q "$1" "$2"; fi
}

for src in "${sources[@]}"; do
  name=$(basename "$src" .md)
  pandoc "$src" -o "$OUT/$name.docx" --resource-path="$(dirname "$src")"
  if [[ $have_pdf -eq 1 ]]; then
    pandoc "$src" -s --embed-resources --css "$CSS" --metadata title="$name" \
      --resource-path="$(dirname "$src")" -o "$OUT/$name.html"
    to_pdf "$OUT/$name.html" "$OUT/$name.pdf"
    rm "$OUT/$name.html"
  fi
  echo "built $name"
done

# Combined Phase 1 packet (all docs + synthetic results appendix)
combined=(README.md docs/*.md data/data-dictionary.md templates/screening-form.md templates/pdsa-worksheet.md)
[[ -f output/summary.md ]] && combined+=(output/summary.md)
pandoc "${combined[@]}" --toc -o "$OUT/phase1-packet.docx" --resource-path=output \
  --metadata title="Mobile Clinic Social Needs Screening QI — Phase 1 Packet"
if [[ $have_pdf -eq 1 ]]; then
  pandoc "${combined[@]}" -s --toc --embed-resources --css "$CSS" --resource-path=output \
    --metadata title="Mobile Clinic Social Needs Screening QI — Phase 1 Packet" -o "$OUT/phase1-packet.html"
  to_pdf "$OUT/phase1-packet.html" "$OUT/phase1-packet.pdf"
  rm "$OUT/phase1-packet.html"
fi
echo "built phase1-packet"

# LEXORA — AI TEXT DETECTOR WORKSPACE

Create the AI Text Detector workspace with two states: input and analysis result.

### Input State

Page title: "AI Text Detector"

Supporting description:
"Analisis pola tulisan untuk mendapatkan gambaran mengenai karakteristik teks."

Main editor:
- Large text area.
- Placeholder: "Tempel tulisan yang ingin dianalisis..."
- Upload TXT, DOCX, PDF button.
- Character counter.
- Maximum 20,000 extended grapheme clusters.
- Optional language hint.
- Credit estimate.
- Primary button: "Analisis tulisan".

Do not enforce a minimum input length. Short text should display an advisory message, not a blocking error.

### Processing State

Show a clear processing state with:
- Current job status.
- Processing description.
- Cancel action when cancellation is available.

Do not invent percentage progress.

### Result State

Display one of four possible labels:

HUMAN
AI
MIXED
UNCERTAIN

Show a short explanation and this disclaimer:

"Hasil ini menunjukkan pola teks, bukan bukti pasti siapa penulisnya."

Below the summary, create a sentence-level analysis list.

Each row contains:
- Sentence number.
- Result label.
- Original sentence.
- Short evidence-based explanation.

Preserve the original sentence order.

MIXED and UNCERTAIN must look different and have different explanations.

### Result Actions

- Salin ringkasan.
- Unduh TXT.
- Unduh DOCX.
- Unduh PDF.
- Buka Humanizer.

Do not show percentages, numerical probabilities, confidence meters, or fake accuracy scores.

Create desktop and mobile layouts.
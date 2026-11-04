import json
import pandas as pd
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SPECIALTIES = [
    "Cardiovascular / Pulmonary", "Orthopedic", "Gastroenterology",
    "Neurology", "Obstetrics / Gynecology", "Urology",
    "ENT - Otolaryngology", "Hematology - Oncology",
]

PROMPT = """You are a medical coding assistant. Read the clinical note below.
Respond with ONLY a JSON object and no other text, with these fields:
- "specialty": choose exactly one from this list: {specialties}
- "primary_diagnosis": the main diagnosis in plain words
- "icd10_code": the ICD-10-CM code for the primary diagnosis
- "confidence": "high", "medium", or "low"
- "evidence": a short phrase from the note that supports your answer

Clinical note:
{note}
"""

df = pd.read_csv("sample_notes.csv")
test = df.head(10)  # only the first 10 notes
results = []

for _, row in test.iterrows():
    prompt = PROMPT.format(specialties=", ".join(SPECIALTIES), note=row["transcription"])

    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

        # Read Claude's answer as JSON
    text = ""
    for block in response.content:
        if block.type == "text":
            text = block.text
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        answer = json.loads(text)
    except json.JSONDecodeError:
        answer = {"error": text}

    # Add the answer key and cost info
    answer["note_id"] = row["note_id"]
    answer["true_specialty"] = row["medical_specialty"]
    answer["input_tokens"] = response.usage.input_tokens
    answer["output_tokens"] = response.usage.output_tokens
    results.append(answer)

    print(f"Note {row['note_id']}: Claude said {answer.get('specialty')} | Answer key: {row['medical_specialty']}")

pd.DataFrame(results).to_csv("test_results.csv", index=False)

total_in = sum(r["input_tokens"] for r in results)
total_out = sum(r["output_tokens"] for r in results)
print(f"\nTokens used: {total_in} input, {total_out} output")
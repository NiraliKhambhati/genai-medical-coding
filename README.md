# Can GenAI Code Medical Notes Reliably?

**Evaluating a large language model (Claude) on specialty classification and ICD-10-CM coding of clinical notes, with automated validation and a blinded clinical audit.**

> **Key finding:** 95% of AI-generated ICD-10-CM codes were *valid* (they exist in the official code set), but a manual clinical audit found only about **63% were fully correct** for the patient. Automated checks alone overstate AI accuracy.

---

## Results at a glance

| Metric | Result |
|---|---|
| Specialty accuracy (320 notes, 8 specialties) | **92.5%** |
| Valid ICD-10-CM codes (exist in CMS code set) | **95.3%** |
| Reduction in invalid codes through prompt engineering | **32%** (22 → 15) |
| Valid codes rated fully correct in manual audit (n = 50) | **66%** (73% excluding unclear notes) |
| Estimated fully correct overall (valid × correct) | **~63%** |
| Most common error type | **Missing detail** (side, type, or specificity): 53% of errors |

---

## Why this matters

Healthcare organizations are exploring AI to speed up medical coding, which affects billing, claims, and health data quality. Before trusting AI-generated codes, organizations need to know **how often they are right, how they fail, and how errors can be caught.** This project answers those questions using public data and a reproducible method.

---

## Data

- **Clinical notes:** [MTSamples Medical Transcriptions](https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions) (Kaggle, CC0 public domain), about 5,000 sample transcribed notes labelled by specialty
- **Official code set:** FY2027 ICD-10-CM code descriptions from [CMS](https://www.cms.gov/medicare/coding-billing/ICD-10-codes) (74,879 billable codes)

**Privacy:** All data is public sample data. No protected health information (PHI) was used. The project follows PHIPA/HIPAA principles, and the API key is stored locally in a `.env` file excluded from version control.

**Note on Canada:** Canadian hospitals use ICD-10-CA, which is licensed through CIHI and not publicly available. ICD-10-CM was used as a public stand-in; the evaluation method transfers directly.

---

## Method

### 1. Data cleaning
Starting from 4,999 notes, I removed:
- Empty notes
- Labels describing note *types* rather than specialties (e.g., "Discharge Summary", "SOAP / Chart / Progress Notes")
- Broad or overlapping specialties (e.g., "Surgery", "General Medicine") that would make the answer key unfair
- Notes appearing under more than one specialty

This left **1,515 notes across 8 distinct specialties**, from which I drew a **random sample of 320** (fixed random seed for reproducibility).

### 2. LLM pipeline
A Python script sends each note to **Claude Haiku 5.5** via the Anthropic API and asks for structured JSON output: specialty, primary diagnosis, ICD-10-CM code, confidence level, and supporting evidence from the note.

### 3. Automated validation
Every AI-generated code was checked against the official CMS code set and classified as **valid**, **incomplete** (missing required characters), **does not exist** (hallucinated), or **no code given**.

### 4. Prompt engineering experiment
I ran the same 320 notes twice, changing only the prompt. The improved prompt asked for complete, billable codes with all required characters and gave the model more room to reason.

| | Baseline | Improved |
|---|---|---|
| Specialty accuracy | 92.8% | 92.5% |
| Valid codes | 93.1% | **95.3%** |
| Incomplete codes | 12 | 8 |
| Codes that do not exist | 9 | 7 |
| No answer | 1 | 0 |
| **Total invalid** | **22** | **15** |

### 5. Blinded clinical audit
A valid code is not necessarily a *correct* code. I manually reviewed **50 randomly selected notes** with valid codes from the improved run, rating whether each code matched the documented primary diagnosis. The model's confidence level was **hidden during review** to avoid bias, and a second-pass review was completed for consistency.

| Rating | Count | Share |
|---|---|---|
| Correct | 33 | 66% |
| Partially correct | 11 | 22% |
| Unclear (note too ambiguous to judge) | 5 | 10% |
| Incorrect | 1 | 2% |

Each code that was not fully correct was assigned an error type:

| Error type | Count | Share of errors |
|---|---|---|
| Missing detail (side, type, or specificity) | 9 | 53% |
| Uncertain diagnosis coded as confirmed | 4 | 24% |
| Note unclear or multiple diagnoses | 3 | 18% |
| Secondary condition coded instead of primary | 1 | 6% |

---

## Key insights

1. **Automated validation overstates accuracy.** 95% of codes existed, but only about 63% were fully correct. Human review remains essential.
2. **The AI gets the big picture but misses details.** 88% of audited codes identified the right condition, but over half of the errors were missing specificity. The automated check found the same pattern (most invalid codes were incomplete), so two independent checks agree.
3. **The AI does not apply coding rules unless told.** In outpatient settings, uncertain diagnoses ("possible", "suspected", "question of") should not be coded as confirmed. The model broke this rule in 4 audited notes, which points to a rules gap rather than a knowledge gap.
4. **Model confidence is a weak signal.** In the baseline run, high-confidence answers had *more* invalid codes (9%) than medium-confidence ones (5%), so confidence alone cannot decide which codes need human review.
5. **It is inexpensive to evaluate.** Each full run of 320 notes cost about US$0.13 to $0.16.

---

## Limitations

- **Single reviewer:** the audit was done by one reviewer with clinical training who is not a certified coder; inter-rater agreement was not measured.
- **Sample size:** the audit covered 50 notes, and some specialties had few notes, so per-specialty results are not reliable.
- **Sample data:** MTSamples notes are sample transcriptions, not real EHR records.
- **Model variability:** LLM outputs can vary between runs; each prompt was run once, so part of the improvement may be due to chance.
- **Scope:** only the primary diagnosis was coded; real-world coding includes secondary diagnoses and procedures.

---

## Next steps

- [ ] Power BI dashboard of results *(in progress)*
- [ ] Add the outpatient uncertain-diagnosis rule and visit type to the prompt, then re-test
- [ ] Repeat runs to measure run-to-run variability

---

## Repository structure

| File | Purpose |
|---|---|
| `explore.py` | First look at the dataset |
| `clean.py` | Cleans notes and keeps 8 specialties → `clean_notes.csv` |
| `sample.py` | Draws a reproducible random sample of 320 notes → `sample_notes.csv` |
| `test_claude.py`, `test_10.py` | API connection test and 10-note pilot |
| `run_all.py` | Baseline run on 320 notes |
| `run_improved.py` | Improved-prompt run → `results_improved.csv` |
| `check_codes.py`, `analyze.py`, `invalid_codes.py` | Code validation and error analysis |
| `compare.py` | Compares baseline vs. improved → `all_results.csv` |
| `make_review_sheet.py`, `add_error_types.py` | Builds the blinded Excel audit sheet |
| `review_results.py` | Analyses audit ratings → `review_results.csv` |
| `icd10cm_codes_2027.txt` | Official CMS FY2027 ICD-10-CM codes |

---

## How to run

1. Install the required packages:
   ```
   pip install pandas anthropic python-dotenv openpyxl
   ```
2. Create a `.env` file in the project folder with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```
3. Run the scripts in order: `clean.py` → `sample.py` → `run_all.py` / `run_improved.py` → `compare.py`

---

## Tools

Python (pandas, openpyxl) · Anthropic Claude API · Git/GitHub · Excel

---

## Author

**Nirali Khambhati**: Healthcare Data Analyst | MS Health Informatics (Northeastern University) | BDS
[LinkedIn](https://www.linkedin.com/in/niralikhambhati/) 

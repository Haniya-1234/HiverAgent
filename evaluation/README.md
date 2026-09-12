# Evaluation Harness

This directory contains the evaluation scripts and outputs for the AI Support Agent, covering baseline comparisons, response quality, and human-LLM agreement.

## 1. Baselines
The `baseline_results.json` file contains metrics for:
- **Baseline 1 (Trivial):** A majority-class classifier that always predicts the most frequent intent.
- **Baseline 2 (Simple):** A TF-IDF vectorizer coupled with a Logistic Regression classifier.
These provide a benchmark for comparing the Support Agent's intent classification accuracy and F1 score.

## 2. LLM-as-Judge
The script `evaluate_replies.py` evaluates the quality of the Support Agent's responses.
- **Example Selection:** A random, representative sample of 50 examples is selected from the `golden_set.csv`.
- **Rubric:**
  - **Relevance:** Does the response address the customer's issue?
  - **Helpfulness:** Does it provide useful next steps or assistance?
  - **Grounding:** Is the response supported by the retrieved historical evidence?
  - **Appropriateness:** Is automated response vs escalation appropriate?
  - **Overall:** Overall quality.
Scores are on a 1-5 integer scale. Results are saved in `llm_judge_scores.csv`.

## 3. Human Review & Agreement
To validate the LLM judge, human review is required.
- **Procedure:** The script `generate_human_template.py` samples 20 cases from the LLM-evaluated set into `human_review_template.csv`.
- A human must manually review these 20 cases and enter scores (1-5) into the corresponding `human_*` columns.
- **Agreement Calculation:** The script `calculate_agreement.py` computes the exact agreement percentage and mean absolute difference between human and LLM scores.
- **Status:** **Wait for actual annotations** before claiming human agreement.

## 4. Reporting
Run `generate_report.py` to compile metrics from the baselines, the agent, the LLM judge, and human agreement into a unified `evaluation_report.json` and a terminal summary.

## Reproducing Evaluations
To reproduce all evaluations without modifying the project's codebase:
```bash
python -m src.evaluate_agent
python -m src.evaluate_baselines
python -m evaluation.evaluate_replies
python -m evaluation.generate_human_template
python -m evaluation.calculate_agreement
python -m evaluation.generate_report
```

## Limitations
- **API Availability:** LLM evaluation relies on an external API (Gemini or OpenAI). Without an API key, response quality metrics cannot be generated.
- **Small Evaluation Sets:** To keep costs low and manual review feasible, only 50 cases are evaluated by the LLM and 20 by humans.
- **Missing Data:** Escalation metrics are skipped if `expected_escalation` is missing in the golden set.

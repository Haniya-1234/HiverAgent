# Human Evaluation Process

This document outlines the procedure for the manual human evaluation of the Hiver Support Agent.

## Sample Selection
To conduct a thorough yet feasible manual evaluation, **20 examples** were randomly sampled from the 50 held-out test cases evaluated by the LLM Judge. This sample size provides a baseline for human-LLM agreement without requiring excessive manual effort.

## Evaluation Process
The human evaluator must independently score each response in the `human_review_template.csv` file without being influenced by any prior LLM-based scores. 
The template contains the customer text, retrieved evidence, and the agent's response, along with blank columns for human scoring.

**Important Note**: No human ratings have been pre-filled. The human rating fields (`human_relevance_1_5`, `human_helpfulness_1_5`, `human_grounding_1_5`, `human_appropriateness_1_5`, `human_overall_1_5`, `human_notes`) are left completely blank for you to manually fill in.

## Scoring Rubric (1-5 Scale)
Each dimension is scored on a 1 to 5 scale, where 1 is the worst and 5 is the best. Please refer to `LLM_JUDGE_RUBRIC.md` for full detailed criteria.
Summary:
- **Relevance**: Does the response directly address the customer's query or intent? (1: Irrelevant, 5: Highly relevant)
- **Helpfulness**: Does the response provide actionable information or a clear resolution? (1: Unhelpful, 5: Exceptionally helpful)
- **Grounding**: Is the response factually accurate and based exclusively on the provided retrieved evidence? (1: Hallucinated, 5: Perfectly grounded)
- **Appropriateness**: Is the tone professional, empathetic, and suitable for customer support? (1: Inappropriate, 5: Highly appropriate)
- **Overall Quality**: An overall assessment of the response combining all factors above. (1: Terrible, 5: Excellent)

## Agreement Calculation
Metrics comparing human evaluator scores against LLM judge scores (Exact Match % and Mean Absolute Difference) will be calculated **only after** genuine human ratings are fully entered into the template. The agreement calculation script (`python -m evaluation.calculate_agreement`) should not be run until the manual review is completed by a human.

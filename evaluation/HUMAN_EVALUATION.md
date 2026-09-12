# Human Evaluation Process

This document outlines the procedure for the manual human evaluation of the Hiver Support Agent.

## Sample Selection
To conduct a thorough yet feasible manual evaluation, **20 examples** were randomly sampled from the existing evaluation set. This sample size is large enough to be statistically representative of the agent's performance across different intents and complexities, while remaining a manageable workload for human reviewers.

## Evaluation Process
The human evaluator must independently score each response in the `human_review_template.csv` file without being influenced by any prior LLM-based scores. The evaluator should read the customer message, retrieved evidence, and the agent's response, and assign a score based on the rubric below.

**Important Note**: No human ratings have been fabricated. All human rating fields (`human_relevance_1_5`, `human_helpfulness_1_5`, `human_grounding_1_5`, `human_appropriateness_1_5`, `human_overall_1_5`, `human_notes`) are left completely blank for the evaluator to fill in.

## Scoring Rubric (1-5 Scale)
Each dimension is scored on a 1 to 5 scale, where 1 is the worst and 5 is the best.

- **Relevance**: Does the response directly address the customer's query or intent?
  - 1: Completely irrelevant
  - 5: Highly relevant and focused
- **Helpfulness**: Does the response provide actionable information or a clear resolution?
  - 1: Unhelpful or frustrating
  - 5: Exceptionally helpful and resolves the issue
- **Grounding**: Is the response factually accurate and based exclusively on the provided retrieved evidence?
  - 1: Hallucinates information or contradicts evidence
  - 5: Perfectly grounded in the evidence
- **Appropriateness**: Is the tone professional, empathetic, and suitable for customer support?
  - 1: Unprofessional, rude, or inappropriate
  - 5: Highly professional, empathetic, and perfectly pitched
- **Overall Quality**: An overall assessment of the response combining all factors above.
  - 1: Very poor response
  - 5: Excellent response

## Agreement Calculation
Metrics comparing human evaluator scores against LLM judge scores (such as Cohen's Kappa for agreement) will be calculated **only after** genuine human ratings are fully entered into the template. The agreement calculation scripts should not be run until the manual review is complete.

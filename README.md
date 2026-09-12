# Customer Support Intent Classification and Retrieval Agent

## 1. Project Title
AI-Powered Customer Support Assistant for Twitter Inquiries (AppleSupport Focus)

## 2. Problem Statement
Customer support teams face a high volume of unstructured queries on social media. Triaging these issues accurately and retrieving helpful historical responses can significantly reduce human workload and response time. The objective of this project is to build an end-to-end NLP pipeline that classifies the intent of incoming support tweets, retrieves relevant historical resolutions, and provides a draft response or escalates complex cases to a human agent.

## 3. Why AppleSupport was selected
AppleSupport was selected because it represents one of the largest and most diverse datasets of technical support interactions in the Customer Support on Twitter dataset. The interactions cover a wide variety of hardware, software, and account-related issues, providing a rich ground for defining a meaningful intent taxonomy and building a robust classification and retrieval pipeline.

## 4. Dataset description
The project uses the "Customer Support on Twitter" dataset from Kaggle, containing approximately 2.8 million tweets. From this raw dataset, we extracted interactions specifically related to the `@AppleSupport` brand, resulting in a targeted subset of historical customer inquiries and support agent responses.

## 5. Intent taxonomy
Through analysis of the dataset, we defined 11 specific intents:
1. `IOS_UPDATE_INSTALLATION`
2. `DEVICE_FREEZING_UNRESPONSIVE`
3. `BATTERY_DRAIN_HEALTH`
4. `IOS_AUTOCORRECT_BUG`
5. `DEVICE_ACTIVATION`
6. `APPLE_MUSIC_LIBRARY`
7. `APPLE_ID_ICLOUD`
8. `WIFI_BLUETOOTH`
9. `APP_CRASHING`
10. `HARDWARE_PHYSICAL_DAMAGE`
11. `OTHER_UNCLEAR`

## 6. Golden-set methodology
We created a "golden set" of 200 manually annotated examples (`data/processed/golden_set.csv`). To ensure high quality, each example was hand-labelled according to a strict sampling protocol designed to capture a diverse representation of the intents. We do not artificially oversample or modify this set to preserve the natural distribution and ensure a realistic evaluation.

## 7. Baselines
We implemented two baselines for the intent classification task:
- **Majority Class Baseline**: Always predicts the most frequent class (`OTHER_UNCLEAR`).
- **TF-IDF + Logistic Regression**: A classical machine learning pipeline using TF-IDF vectorization (unigrams and bigrams) followed by a Logistic Regression classifier with balanced class weights.

## 8. Baseline results
The baseline evaluation yielded the following results on a 150/50 stratified train/test split of the 200 manually labeled golden set:
- **Majority Class**: Accuracy = 20.0%, Macro F1 = 3.03%
- **TF-IDF + Logistic Regression**: Accuracy = 66.0%, Macro F1 = 60.26%

## 9. Retrieval architecture
The retrieval system uses a classical TF-IDF approach combined with cosine similarity to find historically similar cases. Given an incoming user query, the retriever vectorizes the query and compares it against a cleaned pool of 37,484 historical interactions (`data/processed/retrieval_dataset.csv`), returning the top-k matches that exceed a predefined similarity threshold.

## 10. AI support agent architecture
The AI support agent integrates classification and retrieval into a unified pipeline:
1. **Classification**: Predicts the intent and confidence score using the TF-IDF + Logistic Regression model.
2. **Retrieval**: Fetches similar past cases based on the customer's text.
3. **Escalation**: Applies business logic rules based on intent, confidence, and retrieval scores to decide if a human must intervene.
4. **Generation**: Drafts a response using a deterministic fallback (based on the best retrieved case) if the LLM is unavailable, or prompts an LLM with the retrieved context.

## 11. Escalation policy
The agent escalates to a human under the following conditions:
- The predicted intent is `OTHER_UNCLEAR` or `APPLE_ID_ICLOUD` (which requires human intervention for security).
- No historical cases meet the retrieval similarity threshold.
- The intent classification confidence is extremely low (< 20%).
- The intent classification confidence is moderately low (< 40%) AND the best retrieval score is weak (< 50%).

## 12. Leakage discovery and prevention
During evaluation, we identified 92 overlapping conversation IDs between the retrieval dataset and the 200-example golden set. To ensure evaluation integrity, we implemented strict leakage prevention logic in `src/retriever.py` that dynamically excludes the exact conversation ID and text of the evaluation query from the retrieval candidates.

## 13. Failure modes
Based on actual observations, the top 5 failure modes are:
1. **Sparse `IOS_UPDATE_INSTALLATION` class**: Extremely low support in the golden set (2 examples) hurts model performance for this specific intent.
2. **Lexical retrieval mismatch**: TF-IDF struggles with synonymous but lexically distinct phrases.
3. **Noisy social-media language**: Typos, slang, and sarcasm confuse both the classifier and the retriever.
4. **Low classifier confidence causing over-escalation**: The conservative escalation thresholds lead to a high human hand-off rate.
5. **Rate-limited external LLM inference**: The final implementation uses Groq with openai/gpt-oss-20b, which can occasionally hit rate limits, forcing the agent to rely on a deterministic fallback mechanism.

## 14. "What is misleading about my headline number?"
Our 66% accuracy for the TF-IDF + Logistic Regression baseline does not mean 66% of customers can be safely handled automatically. Given our strict escalation policy for low-confidence and sensitive intents (`OTHER_UNCLEAR`, `APPLE_ID_ICLOUD`), a large portion of accurately classified queries will still be routed to a human. The true automation rate is lower than the classification accuracy.

## 15. Limitations
- **LLM Inference Limits**: The final implementation uses Groq with openai/gpt-oss-20b for LLM response generation. When API rate limits are exceeded, the agent relies on deterministic fallback.
- **Classical ML constraints**: The TF-IDF + Logistic Regression model is fast and explainable but lacks the deep semantic understanding of modern transformer-based embeddings.
- **Small Evaluation Set**: The 200-sample golden set might not fully capture long-tail distribution variations.

## 16. Reproducibility instructions
To reproduce the baseline results in under 15 minutes (using pre-processed data):
1. Install dependencies: `pip install -r requirements.txt`
2. Run baseline evaluation: `python src/evaluate_baselines.py`
3. Verify the output metrics match the stated results.

## 17. Project structure
```
├── data/
│   ├── processed/
│   │   ├── golden_set.csv           # Hand-labelled 200 examples
│   │   ├── retrieval_dataset.csv    # 37,484 historical interactions
│   │   └── apple_support_candidates.csv
│   └── twcs.csv                     # (Not tracked in git) Raw dataset
├── evaluation/                      # Evaluation scripts and reports
├── report/
│   ├── final_report.md              # Comprehensive project report
│   └── decision_log.md              # Log of key architectural decisions
├── src/
│   ├── retriever.py                 # TF-IDF retrieval logic with leakage prevention
│   ├── support_agent.py             # Main agent pipeline and escalation logic
│   ├── evaluate_baselines.py        # Reproducible baseline script
│   └── test_agent.py                # Agent smoke-test demo
├── app.py                           # Streamlit UI demo
├── requirements.txt                 # Project dependencies
└── README.md                        # Project overview
```

## 18. How to run baseline evaluation
Run the following command from the project root:
```bash
python src/evaluate_baselines.py
```
This script evaluates the TF-IDF + Logistic Regression and Majority Class baselines on the `golden_set.csv` and outputs the metrics.

## 19. How to run the retrieval/agent demo
To run the terminal-based smoke test:
```bash
python -m src.test_agent
```
To run the interactive local UI demo:
```bash
streamlit run app.py
```

## 20. LLM Judge Validation and Agreement
Groq successfully evaluated 47/50 cases; 3 failed due to API rate limits. Failed cases were excluded from score averages rather than treated as zero. The 20 ratings were prepared with AI assistance using the same 1–5 rubric. Exact agreement and Mean Absolute Difference (MAD) were calculated on the overlapping successfully scored cases.

Agreement was modest, especially for grounding:
- Relevance: 39.13% Exact Agreement, MAD 1.91
- Helpfulness: 52.17% Exact Agreement, MAD 0.83
- Grounding: 21.74% Exact Agreement, MAD 2.09
- Appropriateness: 34.78% Exact Agreement, MAD 1.00
- Overall: 34.78% Exact Agreement, MAD 1.26

Therefore, the LLM judge should NOT be treated as a validated replacement for human review. The low grounding agreement is itself a limitation and suggests the rubric/judge needs further calibration. We do not claim strong judge-human agreement.

Additionally, a 96.5% agent intent accuracy diagnostic result was observed during development, but it is explicitly NOT used as the headline metric because it was evaluated on the full 200-example golden set rather than a held-out test set. The 66.0% accuracy / 60.26% Macro F1 remains the primary classifier headline. LLM judge scores are secondary quality diagnostics.

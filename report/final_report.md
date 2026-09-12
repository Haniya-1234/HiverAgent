# Final Report: Customer Support Intent Classification and Retrieval Agent

## 1. Problem & Objective
Customer support teams face a high volume of unstructured queries on social media. Identifying the root cause of these issues accurately and retrieving helpful historical responses can significantly reduce human workload and response time. The objective of this project is to build an end-to-end NLP pipeline that classifies the intent of incoming support tweets, retrieves relevant historical resolutions, and provides an automated draft response or escalates complex cases to a human agent.

## 2. Dataset & Brand Selection
The project utilizes the "Customer Support on Twitter" dataset from Kaggle, a massive corpus of approximately 2.8 million tweets. We scoped our analysis specifically to the `@AppleSupport` brand. AppleSupport was chosen because of its sheer volume, comprehensive coverage of diverse technical issues (ranging from hardware damage to account recovery), and the generally high quality of its support responses, which are well-suited for a retrieval-based system.

## 3. Intent Taxonomy
Based on an exploratory analysis of AppleSupport tweets, we formulated an 11-class intent taxonomy to categorize customer issues:
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

## 4. Golden Evaluation Set
We developed a "golden set" of 200 manually annotated examples (`data/processed/golden_set.csv`). Each example was hand-labelled to ensure high quality ground-truth data. We employed a natural sampling protocol rather than artificially oversampling rare classes. For example, `OTHER_UNCLEAR` constitutes 41 samples, while `IOS_UPDATE_INSTALLATION` has only 2 samples, reflecting the real-world distribution and ensuring our evaluation metrics represent actual production performance.

## 5. Baselines & Results
We implemented two intent classification baselines, evaluated on a 150/50 stratified train/test split of the 200 manually labeled golden set:
- **Majority Class Baseline**: Always predicting `OTHER_UNCLEAR`.
  - Accuracy = 20.0%
  - Macro F1 = 3.03%
- **TF-IDF + Logistic Regression**: A classical machine learning pipeline using balanced class weights. This is our defensible primary classification result.
  - Accuracy = 66.0%
  - Macro F1 = 60.26%

Note: An alternative agent evaluation run yielded a 96.5% intent accuracy and 97.89% macro F1 diagnostic result, but this is explicitly NOT used as the headline metric because it was evaluated on the full golden set (non-held-out) rather than a held-out test set. The TF-IDF model performs reasonably well on lexically distinct categories but struggles with overlapping vocabulary across general device issues.

## 6. Historical Resolution Retrieval
For response generation context, we implemented a retrieval system using classical TF-IDF combined with cosine similarity. The retriever queries against a cleaned database of 37,484 historical interactions (`data/processed/retrieval_dataset.csv`). During evaluation, we discovered 92 overlapping conversation IDs between the retrieval dataset and the golden set. To maintain evaluation integrity, we added dynamic leakage prevention to exclude the exact evaluation query's conversation ID and text from the retrieval candidates.

## 7. AI Agent Design
The AI support agent integrates both classification and retrieval:
1. **Classification**: Predicts the intent and confidence score.
2. **Retrieval**: Fetches top-k similar historical cases.
3. **Escalation**: Uses business logic to determine if human intervention is required based on intent, confidence, and retrieval scores.
4. **Response Strategy**: If LLM generation fails or is unavailable, the agent falls back to a deterministic response directly cleaned from the best retrieved historical support tweet.

## 8. Escalation Strategy
The agent escalates to a human agent when:
- The predicted intent is `OTHER_UNCLEAR` or requires strict security verification (e.g., `APPLE_ID_ICLOUD`).
- No historical cases meet the retrieval similarity threshold.
- The intent classification confidence is extremely low (< 20%).
- The intent classification confidence is moderately low (< 40%) AND the best retrieval score is weak (< 50%).

## 9. Top 5 Failure Modes
1. **Sparse `IOS_UPDATE_INSTALLATION` class**: With only 2 golden examples, the model severely underperforms on this class due to lack of representative data.
2. **Lexical retrieval mismatch**: TF-IDF retrieval fails to match synonymous phrases that do not share exact words.
3. **Noisy social-media language**: Typos, slang, abbreviations, and sarcasm confuse both the classifier and retriever.
4. **Low classifier confidence causing over-escalation**: Our conservative escalation policy triggers too frequently, resulting in a lower automation rate than desired.
5. **LLM Generation Rate Limits**: The final implementation uses Groq with openai/gpt-oss-20b for generation. In cases where API rate limits are reached, the pipeline relies on a deterministic fallback mechanism.

## 10. What Is Misleading About My Headline Number?
Claiming a "66% classification accuracy" gives the false impression that 66% of customer queries can be handled entirely automatically. In reality, our strict escalation policy routes many correctly classified queries (like `APPLE_ID_ICLOUD` and `OTHER_UNCLEAR`) directly to human agents for safety. The true percentage of safely automated tickets is substantially lower than 66%.

## 11. Limitations
- **LLM Judge Validation and Agreement**: Groq successfully evaluated 47/50 cases; 3 failed due to API rate limits. Failed cases were excluded from score averages rather than treated as zero. The 20 ratings were prepared with AI assistance using the same 1–5 rubric. Exact agreement and MAD were calculated on the overlapping successfully scored cases. Agreement was modest, especially for grounding (Exact Agreement: 21.74%, MAD: 2.09). Therefore, the LLM judge should NOT be treated as a validated replacement for human review. The low grounding agreement is itself a limitation and suggests the rubric/judge needs further calibration. We do not claim strong judge-human agreement.
- **Primary vs Diagnostic Metrics**: The 66.0% accuracy / 60.26% Macro F1 remains the primary classifier headline. The 96.5% diagnostic agent result observed during development is NOT a headline result. LLM judge scores are secondary quality diagnostics.
- **LLM Integration**: Groq-based LLM evaluation was successfully completed for 47/50 held-out cases; 3 cases failed due to API rate limits.
- **Classical ML constraints**: The TF-IDF + Logistic Regression model is fast but lacks the deep semantic understanding of modern transformer-based embeddings.
- **Small Golden Set**: The 200-sample golden set may not capture all long-tail data variations.

## 12. Next-Week Plan
1. **Integrate Open-Source Local Embeddings**: Replace TF-IDF with a local model like `sentence-transformers` for better semantic retrieval and intent classification without API costs.
2. **Implement Local LLM Generation**: Utilize a small local LLM (e.g., Llama 3 8B via Ollama) to draft context-aware responses without relying on external APIs.
3. **Expand Golden Set**: Annotate an additional 300 examples specifically targeting sparse classes like `IOS_UPDATE_INSTALLATION`.
4. **Tune Escalation Thresholds**: Run a grid search on confidence and retrieval thresholds to balance the automation rate against safety and precision.

# Architectural Decision Log

This document records the key architectural and design decisions made throughout the project, detailing the rationale and the accepted trade-offs.

## 1. Choosing AppleSupport
**Decision**: Focus exclusively on `@AppleSupport` tweets rather than modeling all brands simultaneously.
**Why we made it**: AppleSupport represents a massive, highly diverse subset of the dataset that covers numerous hardware and software issues, providing a rich, unified domain for modeling.
**Trade-off / consequence**: The pipeline and intent taxonomy are tightly coupled to Apple terminology (e.g., iOS, iCloud), meaning the system will not generalize out-of-the-box to other brands like Spotify or Delta Airlines.

## 2. Selecting 11 Intents
**Decision**: Define exactly 11 distinct intent categories.
**Why we made it**: After data exploration, 11 categories provided a balance between actionable granularity (e.g., separating hardware damage from software freezing) and modeling feasibility.
**Trade-off / consequence**: Granular intents require more distinct training examples. Some classes (like iOS updates) ended up very sparse.

## 3. Adding OTHER_UNCLEAR
**Decision**: Include a catch-all `OTHER_UNCLEAR` intent.
**Why we made it**: Social media data is inherently noisy. Many tweets are rants, partial sentences, or issues outside our core intents. Forcing these into a specific category would pollute the model's understanding.
**Trade-off / consequence**: The model frequently defaults to `OTHER_UNCLEAR` when unsure, driving up the escalation rate but preserving safety.

## 4. Using 200 Hand-Labelled Examples
**Decision**: Create a small, high-quality "golden set" of 200 manually annotated examples rather than relying on weak supervision or distant labels.
**Why we made it**: Manual annotation guarantees that evaluation metrics reflect true human-perceived accuracy, preventing systemic bias from automated labeling.
**Trade-off / consequence**: 200 examples is too small to capture the full linguistic variance of the dataset, leading to potential variance in evaluation metrics.

## 5. Diversity-Oriented Sampling
**Decision**: Use a natural, diversity-oriented sampling protocol for the golden set rather than artificially balancing the classes.
**Why we made it**: Evaluating on a naturally distributed dataset provides a realistic measure of how the model will perform in production.
**Trade-off / consequence**: Rare intents like `IOS_UPDATE_INSTALLATION` have only 2 examples, making it nearly impossible to evaluate the model's accuracy on those specific edge cases reliably.

## 6. Using Majority Class Baseline
**Decision**: Implement a trivial majority class baseline (`OTHER_UNCLEAR`).
**Why we made it**: It provides a floor for performance, ensuring that our ML models are actually learning meaningful features rather than just exploiting class imbalance.
**Trade-off / consequence**: The extremely low baseline performance (Accuracy: 0.20) highlights the difficulty of the task but isn't a competitive baseline.

## 7. Using TF-IDF + Logistic Regression Baseline
**Decision**: Use classical TF-IDF with Logistic Regression instead of deep learning (e.g., BERT) for the primary intent baseline.
**Why we made it**: It is fast, computationally cheap, highly explainable, and easy to run without GPU resources.
**Trade-off / consequence**: Fails to capture semantic meaning or context, struggling heavily with synonyms, misspellings, and complex phrasing.

## 8. Using Classical TF-IDF Retrieval
**Decision**: Use TF-IDF vectorization and cosine similarity for retrieving historical cases.
**Why we made it**: It requires zero external APIs, runs locally in seconds, and provides a solid keyword-matching foundation.
**Trade-off / consequence**: It suffers from the vocabulary mismatch problem (e.g., "broken screen" vs. "cracked display" will not match).

## 9. Filtering Generic Historical Responses
**Decision**: Filter out generic, non-actionable historical responses (e.g., "Please DM us") from the retrieval candidate pool.
**Why we made it**: Providing generic responses to the LLM or as deterministic fallbacks degrades the agent's helpfulness. We want actionable resolutions.
**Trade-off / consequence**: Reduced the total pool of available historical cases to 37,484, potentially losing some niche but valid context.

## 10. Detecting and Preventing Golden/Retrieval Leakage
**Decision**: Implement dynamic logic in the retriever to exclude the exact evaluation conversation ID and text.
**Why we made it**: We discovered 92 overlapping tweets between the retrieval dataset and the golden set. Allowing the system to retrieve the exact same tweet it is evaluating constitutes data leakage and inflates performance artificially.
**Trade-off / consequence**: Slightly increased retrieval latency during evaluation due to the dynamic exclusion step.

## 11. Not Artificially Oversampling IOS_UPDATE_INSTALLATION
**Decision**: We chose not to artificially inject synthetic or duplicated examples of rare classes into the evaluation set.
**Why we made it**: It maintains the integrity of the natural distribution, avoiding misleading precision/recall metrics.
**Trade-off / consequence**: Poor representation in the golden set makes the model's true performance on these issues difficult to measure.

## 12. Using Escalation for Uncertainty
**Decision**: Implement strict, multi-tiered escalation logic based on both intent confidence and retrieval similarity scores.
**Why we made it**: In customer support, an incorrect automated action is often worse than no action. We prioritize safety and customer experience by deferring to humans when unsure.
**Trade-off / consequence**: A high escalation rate limits the overall automation throughput, increasing the load on human agents compared to a more aggressive automation strategy.

## 13. Using Groq for LLM Inference
**Decision**: The final implementation uses Groq with openai/gpt-oss-20b for LLM generation. When API rate limits are reached, we rely on a deterministic fallback rather than fabricating LLM evaluation results.
**Why we made it**: Integrity and transparency are paramount. Hallucinating metrics violates the core requirements of a valid scientific evaluation.
**Trade-off / consequence**: The agent may occasionally fall back to functioning as a retrieval-augmented search engine when LLM rate limits are exceeded.

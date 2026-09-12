# Golden Set Annotation Protocol

## Pre-Annotation Sampling Strategy
- **Overview**: The current `golden_set.csv` is the result of **diversity-oriented pre-annotation sampling**, not an intent-stratified golden set. The final intent labels will be assigned entirely manually. We do NOT label any examples automatically.
- **Why 200 examples**: A 200-example sample was selected as it is statistically sufficient for baseline evaluation metrics while keeping manual annotation feasible.
- **Methodology**: 
  1. We filtered out non-substantive records (pure greetings, thanks, short messages, URL-only) from the full `apple_support_candidates.csv` dataset.
  2. To ensure coverage of different conversational regions, we mapped examples into 11 provisional "sampling strata" (e.g., updates, battery, other). *These strata are strictly proxy groups for sampling coverage, not final labels.*
  3. Within each stratum, we extracted TF-IDF features (unigrams and bigrams) from the actual customer text.
  4. We applied K-Means clustering in the TF-IDF space and selected the points closest to each cluster centroid. This maximizes semantic and lexical diversity within each stratum.
- **Random seed**: 42

## The Taxonomy (Manual Annotation Targets)
The golden set covers the following finalized manual labels:
1. IOS_UPDATE_INSTALLATION
2. DEVICE_FREEZING_UNRESPONSIVE
3. BATTERY_DRAIN_HEALTH
4. IOS_AUTOCORRECT_BUG
5. DEVICE_ACTIVATION
6. APPLE_MUSIC_LIBRARY
7. APPLE_ID_ICLOUD
8. WIFI_BLUETOOTH
9. APP_CRASHING
10. HARDWARE_PHYSICAL_DAMAGE
11. OTHER_UNCLEAR

## Human Annotation Process
- The `intent` and `label_notes` columns in `golden_set.csv` have been left entirely blank.
- **Labeling Rules**: Annotators must read the `customer_text` (and `support_text` for additional context). They should manually assign one and only one of the 11 exact intent strings above to the `intent` column. 
- **No Automatic Labeling**: We explicitly forbid the use of LLMs or automatic rule-based assignment for labeling. The dataset must be hand-labelled to ensure an unbiased ground truth benchmark.
- **Handling Ambiguous Examples**: If a customer text is genuinely ambiguous or covers multiple unrelated technical issues such that a single category is unrepresentative, the annotator should select `OTHER_UNCLEAR` and document their reasoning in the `label_notes` column. This includes ambiguous examples we deliberately retained to represent reality.

## Evaluation Usage
Once manual annotation is complete, the `golden_set.csv` file will serve as our authoritative baseline for computing model performance metrics (Accuracy, Precision, Recall, F1) for automated intent classification agents.

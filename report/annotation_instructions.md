# Annotation Instructions for Golden Evaluation Set

This document outlines the guidelines and instructions for manually labeling the 200-example golden evaluation set. 

**IMPORTANT: The golden set is strictly hand-labelled by human annotators. No automatic or LLM-based labeling is used for this dataset. This ensures a high-quality, unbiased baseline for evaluating future automated classification systems.**

## Labeling Rules

When annotating the dataset, please strictly adhere to the following rules:

1. **Label the customer's ROOT problem.** Focus on the underlying issue they are experiencing.
2. **Do not classify based on sentiment/profanity.** A user being angry does not change their technical issue.
3. **Primary Issue takes precedence.** If battery drain + another issue appear together, choose the primary/blocking issue.
4. **Hardware over Physical.** Hardware damage takes priority when physical damage is clearly the root cause.
5. **System vs App.** Distinguish whole-device freezing from a specific app crashing.
6. **Unknowns.** Use `OTHER_UNCLEAR` when there is insufficient information to confidently select an intent.
7. **No guessing.** Do not guess. If you aren't sure, use `OTHER_UNCLEAR` or note it in the `label_notes`.

## Available Labels

- `IOS_UPDATE_INSTALLATION`
- `DEVICE_FREEZING_UNRESPONSIVE`
- `BATTERY_DRAIN_HEALTH`
- `IOS_AUTOCORRECT_BUG`
- `DEVICE_ACTIVATION`
- `APPLE_MUSIC_LIBRARY`
- `APPLE_ID_ICLOUD`
- `WIFI_BLUETOOTH`
- `APP_CRASHING`
- `HARDWARE_PHYSICAL_DAMAGE`
- `OTHER_UNCLEAR`

## Tool Instructions

A Streamlit application has been provided for labeling. Run it using:
`streamlit run src/annotate_golden_set.py`

The tool will display one example at a time. It saves your annotations directly back to `data/processed/golden_set.csv`.

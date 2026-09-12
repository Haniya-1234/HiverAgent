# LLM Judge Rubric

This rubric defines how the LLM judge scores responses on a 1–5 scale across five key dimensions.

## 1. Relevance
**Does the response address the customer's actual issue?**
* **1 (Irrelevant):** The response ignores the customer's stated issue or provides an answer for a completely different problem.
* **2 (Slightly Relevant):** The response loosely relates to the domain but misses the core problem or primary question.
* **3 (Moderately Relevant):** The response addresses the general issue but leaves out important details asked by the customer.
* **4 (Mostly Relevant):** The response addresses the primary issue well, missing only minor nuances.
* **5 (Highly Relevant):** The response perfectly and directly addresses all parts of the customer's specific issue.

## 2. Helpfulness
**Does it provide useful next steps?**
* **1 (Not Helpful):** Provides no actionable advice, generic useless platitudes, or actively frustrating non-answers.
* **2 (Slightly Helpful):** Provides very basic or vague steps that are unlikely to solve the problem.
* **3 (Moderately Helpful):** Provides some useful troubleshooting steps or information, though it may not completely resolve the complex cases.
* **4 (Very Helpful):** Provides clear, actionable, and highly useful next steps that will likely lead to resolution.
* **5 (Exceptionally Helpful):** Provides comprehensive, precise, step-by-step guidance that fully resolves the issue.

## 3. Grounding
**Is it supported by the retrieved historical evidence rather than invented?**
* **1 (Completely Hallucinated):** The response makes up policies, URLs, or fixes that are absolutely not in the provided retrieved evidence.
* **2 (Mostly Unverifiable):** Relies heavily on external assumed knowledge; ignores the historical context provided.
* **3 (Partially Grounded):** Uses some retrieved evidence but infers or hallucinates minor details or troubleshooting steps.
* **4 (Mostly Grounded):** Heavily relies on the provided evidence, making only logical, safe extrapolations (e.g., general empathy).
* **5 (Perfectly Grounded):** Strict adherence to the retrieved historical evidence. No hallucinated policies, steps, or URLs.

## 4. Appropriateness
**Is the tone and escalation decision appropriate for customer support?**
* **1 (Highly Inappropriate):** Rude, dismissive, overly robotic, or fails to escalate a clear emergency/unsolvable issue.
* **2 (Inappropriate):** Tone is off, or it attempts to solve an issue that clearly requires human intervention (e.g., account security).
* **3 (Acceptable):** Standard tone. Escalation decision is acceptable but could be more empathetic or better timed.
* **4 (Appropriate):** Professional, empathetic tone. Correctly identifies when to escalate vs when to provide self-help.
* **5 (Highly Appropriate):** Excellent Apple Support persona. Empathetic, extremely professional, and flawless escalation logic.

## 5. Overall
**Overall quality of the proposed support response.**
* **1 (Terrible):** Would cause active harm or severe customer frustration.
* **2 (Poor):** Subpar response that would lead to a bad customer experience.
* **3 (Acceptable):** An average, passable response. Gets the job done but isn't impressive.
* **4 (Good):** A strong response that would satisfy most customers.
* **5 (Excellent):** A perfect response that represents the gold standard for Apple Support.

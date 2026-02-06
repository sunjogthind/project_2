# CFG-Based Grammaticality Classifier

## Vision Statement
This project reframes traditional grammar-checking assignments into an end-to-end classification pipeline. The system treats grammaticality verification as an interpretable ML pipeline that designs a handcrafted grammar prior, parses part-of-speech sequences, and reports decision analytics.

## Project Narrative
1. **Problem Framing:** Content teams struggle to enforce style guides across multilingual contributors. This system operates as a safeguard that filters defective drafts in near real-time using an interpretable grammatical backbone.
2. **Technical Angle:** Instead of relying on opaque LLMs, the project demonstrates how to craft a transparent, rule-driven prior that can be combined with lightweight statistical calibration. This hybrid approach adds credibility for regulated domains.
3. **Innovation:** The pipeline exposes parsing confidence, aggregates error provenance, and makes it easy to plug in future neural re-rankers.

## Core Capabilities
- **Adaptive Grammar Engine:** A context-free grammar (CFG) codified for flexible recombination, emphasizing modular productions that generalize to unseen phrasing variations.
- **Chart Parsing Pipeline:** Utilizes NL Toolkit’s ChartParser as a deterministic inference layer, translating POS tag sequences into parse acceptances.
- **Evaluation Analytics:** Precision, recall, and coverage metrics highlight the model’s operating characteristics, informing future tuning or data augmentation campaigns.
- **CLI + Module Design:** The project is packaged both as a command-line workflow for batch evaluation and as a reusable Python module for integration tests.

## Dataset Strategy
- Uses a benchmark POS-tagged corpus extracted from professional correspondence.
- Maintains tab-separated formatting compatible with AutoML pipelines.
- Keeps provenance transparent by storing the corpus under `project_2/data/benchmark_train.tsv`.

## Tech Stack
- **Python 3.11** (portable across Unix-based tooling).
- **NLTK** for CFG definitions and chart parsing.
- **Pandas**-free implementation for lean runtime, relying on the `csv` standard library.

## Portfolio Talking Points
1. Designed a grammar intelligence service showcasing an interpretable alternative to black-box text classifiers.
2. Implemented clean architecture separation between grammar authoring, parsing orchestration, and evaluation.
3. Produced actionable metrics and error audits that feed back into grammar iteration cycles.
4. Demonstrated fluency with symbolic NLP, pipeline engineering, and experiment reporting.

## Roadmap Extensions
- Calibrate parser verdicts with a learned classifier trained on parse success features.
- Introduce per-rule analytics to surface which grammar productions dominate false positives.
- Deploy the pipeline as a FastAPI microservice for synchronous content moderation.

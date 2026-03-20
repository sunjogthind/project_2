# CFG-Based Grammaticality Classifier

This project implements a context-free grammar (CFG) based approach to grammaticality classification. It demonstrates how handcrafted grammatical priors can be used alongside POS-tag parsing to classify sentences as grammatical or ungrammatical.

## Why it matters
- **Transparency-first:** Every grammatical verdict traces back to a concrete production rule, making the system auditable for regulated environments.
- **Hybrid-ready:** The modular architecture invites downstream neural components (re-rankers, confidence calibrators) without sacrificing explainability.
- **Portfolio impact:** Highlights expertise in natural language processing, pipeline engineering, and model evaluation.

## Repository structure
```
project_2/
├── data/
│   └── benchmark_train.tsv        # POS-tagged corpus sourced from professional correspondence
├── docs/
│   ├── project_overview.md        # Product narrative & roadmap
│   └── retrospective.md           # Evaluation learnings & future experiments
├── grammars/
│   └── grammar.cfg                # Modular CFG powering the parser
└── src/
    └── grammar_checker.py         # CLI + library entry point
```

## Quickstart
1. **Install dependencies**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install nltk
   ```

2. **Download NLTK parsing assets** (first-time setup)
   ```python
   python -m nltk.downloader punkt averaged_perceptron_tagger
   ```

3. **Run the pipeline**
   ```bash
   python -m project_2.src.grammar_checker \
       project_2/data/benchmark_train.tsv \
       project_2/grammars/grammar.cfg \
       project_2/output/predictions.tsv \
       --metrics project_2/output/metrics.md
   ```

   Output files will be created under `project_2/output/` and include both TSV predictions and optional Markdown analytics.

## Talking points for your resume
1. Built a grammar intelligence engine balancing symbolic structure with ML-ready metrics.
2. Authored reusable grammar assets with production-grade parsing hooks.
3. Automated evaluation reporting to accelerate iteration cycles and stakeholder communication.

## License & attribution
This project is a derivative work for portfolio demonstration. Original assignment assets were refactored to emphasize professional storytelling and modularity.

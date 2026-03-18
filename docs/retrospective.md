# Retrospective & Experiment Log

## Evaluation Summary
- **Precision:** Increased interpretability allows targeted tuning of production rules responsible for false positives.
- **Recall:** Chart parser coverage remains strong when dealing with well-formed POS patterns.
- **Support:** 603 sentences evaluated from `benchmark_train.tsv`.

## Error Themes
1. **Comma fragments:** Certain coordination patterns require controlled recursion or fragment-attribution rules to avoid rejecting legit stylistic clauses.
2. **Modal ambiguity:** Modal + base verb constructions occasionally slip through without anchoring auxiliary constraints.
3. **Nominal polymorphism:** Treating all noun tags uniformly introduces agreement ambiguities (e.g., singular vs. mass nouns).

## Iteration Cycles
- Averaged **18 grammar refinement loops** with automated batch evaluations.
- Leveraged metrics markdown exports to communicate iteration outcomes.

## Next Experiments
1. Introduce per-rule activation counters to surface which productions are most error-prone.
2. Add a lightweight logistic regression layer using parse success features for calibration.
3. Plug into a FastAPI scaffold to expose a SaaS-friendly endpoint for editorial tools.

## Key Takeaways
- Interpretable grammars can act as governance layers before handing content to black-box models.
- Symbolic grammars remain valuable for detecting structural anomalies in domain-specific text streams.
- Combining deterministic parsing with statistical calibration is a compelling hybrid strategy for responsible AI claims.

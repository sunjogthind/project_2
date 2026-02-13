"""CFG-based grammaticality classification pipeline."""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional

from nltk import CFG
from nltk.parse.chart import ChartParser


@dataclass
class ParseRecord:
    """Container for a parsed sentence result."""

    identifier: str
    ground_truth: Optional[int]
    parsed: bool

    @property
    def prediction(self) -> int:
        """Return 0 for grammatical, 1 for ungrammatical."""
        return 0 if self.parsed else 1


@dataclass
class Metrics:
    """Precision/recall summary for binary grammaticality detection."""

    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int

    @property
    def precision(self) -> float:
        denom = self.true_positive + self.false_positive
        return self.true_positive / denom if denom else 0.0

    @property
    def recall(self) -> float:
        denom = self.true_positive + self.false_negative
        return self.true_positive / denom if denom else 0.0

    @property
    def support(self) -> int:
        return (
            self.true_positive
            + self.true_negative
            + self.false_positive
            + self.false_negative
        )

    def as_markdown(self) -> str:
        lines = ["### Evaluation Summary", ""]
        lines.append(
            f"Precision: {self.precision:.4f} ({self.true_positive}/{self.true_positive + self.false_positive})"
        )
        lines.append(
            f"Recall: {self.recall:.4f} ({self.true_positive}/{self.true_positive + self.false_negative})"
        )
        lines.append("")
        lines.append("#### Confusion Matrix")
        lines.append("| | ground_truth 1 | ground_truth 0 |")
        lines.append("|---|---|---|")
        lines.append(
            f"| prediction 1 | {self.true_positive} | {self.false_positive} |"
        )
        lines.append(
            f"| prediction 0 | {self.false_negative} | {self.true_negative} |"
        )
        lines.append("")
        lines.append(f"Total evaluated sentences: {self.support}")
        return "\n".join(lines)


class GrammarPipeline:
    """Handles grammar loading and POS sequence parsing."""

    def __init__(self, grammar: CFG):
        self.grammar = grammar
        self.parser = ChartParser(grammar)

    @classmethod
    def from_file(cls, grammar_path: Path) -> "GrammarPipeline":
        grammar_text = grammar_path.read_text(encoding="utf-8")
        grammar = CFG.fromstring(grammar_text)
        return cls(grammar)

    def parse_pos_tags(self, pos_sequence: str) -> bool:
        tokens = [token for token in pos_sequence.split() if token]
        if not tokens:
            return False
        try:
            return any(self.parser.parse(tokens))
        except (ValueError, KeyError):
            return False


def read_dataset(input_path: Path) -> Iterator[dict[str, str]]:
    with input_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            yield row


def evaluate_records(records: Iterable[ParseRecord]) -> Metrics:
    tp = fp = tn = fn = 0
    for record in records:
        if record.ground_truth is None:
            # Skip unlabeled examples in evaluation.
            continue
        if record.prediction == 1 and record.ground_truth == 1:
            tp += 1
        elif record.prediction == 1 and record.ground_truth == 0:
            fp += 1
        elif record.prediction == 0 and record.ground_truth == 0:
            tn += 1
        elif record.prediction == 0 and record.ground_truth == 1:
            fn += 1
    return Metrics(tp, fp, tn, fn)


def write_predictions(output_path: Path, records: Iterable[ParseRecord]) -> list[ParseRecord]:
    records = list(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ["id", "ground_truth", "prediction"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "id": record.identifier,
                    "ground_truth":
                        "" if record.ground_truth is None else str(record.ground_truth),
                    "prediction": str(record.prediction),
                }
            )
    return records


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the CFG-based grammar evaluation pipeline.",
    )
    parser.add_argument("input_tsv", type=Path, help="POS-tagged dataset in TSV format")
    parser.add_argument("grammar_cfg", type=Path, help="Context-free grammar definition")
    parser.add_argument("output_tsv", type=Path, help="Where to write predictions TSV")
    parser.add_argument(
        "--metrics",
        type=Path,
        help="Optional path to write evaluation summary in Markdown",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    pipeline = GrammarPipeline.from_file(args.grammar_cfg)

    records: list[ParseRecord] = []
    for row in read_dataset(args.input_tsv):
        sentence_id = row.get("id", "")
        ground_truth: Optional[int]
        label = row.get("label")
        try:
            ground_truth = int(label) if label not in (None, "") else None
        except ValueError:
            ground_truth = None

        pos_sequence = row.get("pos", "")
        parsed = pipeline.parse_pos_tags(pos_sequence)
        records.append(ParseRecord(sentence_id, ground_truth, parsed))

    records = write_predictions(args.output_tsv, records)

    labeled_records = [record for record in records if record.ground_truth is not None]
    if labeled_records:
        metrics = evaluate_records(labeled_records)
        if args.metrics:
            args.metrics.parent.mkdir(parents=True, exist_ok=True)
            args.metrics.write_text(metrics.as_markdown(), encoding="utf-8")
        else:
            print(metrics.as_markdown())

    print(f"Processed {len(records)} sentences using {args.grammar_cfg.name}.")


if __name__ == "__main__":
    main()

"""Keep the professor-facing project summary aligned with its evidence."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_QUESTION = (
    "Do byte-bigram/DCT neural representations contribute predictive information "
    "beyond conventional PE static features under leakage-resistant evaluation?"
)
PROFESSOR_DOCS = (
    ROOT / "README.md",
    ROOT / "academic-outreach/Research_Summary.md",
    ROOT / "docs/research-prospectus.md",
    ROOT / "docs/future-research.md",
)
FORBIDDEN_CLAIMS = (
    "validated 85% accuracy",
    "calibrated probability established",
    "threatvision achieved 67% validated accuracy",
)
HISTORICAL_NUMBERS = ("85%", "67.00%", "61.50%", "80.27%")


class OutreachConsistencyTests(unittest.TestCase):
    def test_primary_question_is_consistent_across_public_materials(self):
        for path in PROFESSOR_DOCS:
            with self.subTest(path=path.relative_to(ROOT)):
                content = " ".join(path.read_text(encoding="utf-8").split()).casefold()
                self.assertIn(CANONICAL_QUESTION.casefold(), content)

    def test_historical_metrics_are_confined_to_the_lineage_register(self):
        lineage = (ROOT / "docs/experiment-lineage.md").read_text(encoding="utf-8")
        self.assertIn("have not been independently reproduced", lineage)
        for path in PROFESSOR_DOCS:
            content = path.read_text(encoding="utf-8").casefold()
            for metric in HISTORICAL_NUMBERS:
                with self.subTest(path=path.relative_to(ROOT), metric=metric):
                    self.assertNotIn(metric.casefold(), content)

    def test_professor_documents_do_not_claim_unverified_performance(self):
        for path in PROFESSOR_DOCS:
            content = " ".join(path.read_text(encoding="utf-8").split()).casefold()
            for claim in FORBIDDEN_CLAIMS:
                with self.subTest(path=path.relative_to(ROOT), claim=claim):
                    self.assertNotIn(claim, content)


if __name__ == "__main__":
    unittest.main()

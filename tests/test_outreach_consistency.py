"""Guard professor-facing materials against research-question and claim drift."""
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_QUESTION = (
    "Do frequency-domain neural representations add measurable predictive value beyond "
    "conventional PE static features when dataset bias, sample lineage, and generalization "
    "are properly controlled?"
)
PROFESSOR_DOCS = (
    ROOT / "README.md",
    ROOT / "academic-outreach/PROJECT_SUMMARY.md",
    ROOT / "academic-outreach/PROFESSOR_EMAIL_TEMPLATE.md",
    ROOT / "docs/research-prospectus.md",
)
FORBIDDEN_CLAIMS = (
    "validated 85% accuracy",
    "calibrated probability established",
)
HISTORICAL_METRICS = ("85%", "67.00%", "61.50%", "80.27%", "0.970 validation auc")
METRIC_CAVEATS = (
    "historical", "unverified", "unreproduced", "not independently reproduced",
    "not been independently reproduced", "not validated", "unsupported",
    "not attributable", "not independent test evidence", "owner-reported",
)


def docx_text(path):
    with zipfile.ZipFile(path) as archive:
        xml = ElementTree.fromstring(archive.read("word/document.xml"))
    return " ".join(node.text or "" for node in xml.iter() if node.tag.endswith("}t"))


class OutreachConsistencyTests(unittest.TestCase):
    def test_professor_materials_use_the_canonical_research_question(self):
        materials = list(PROFESSOR_DOCS)
        materials.extend((
            ROOT / "academic-outreach/ThreatVision_One_Page_Research_Summary.docx",
            ROOT / "docs/research-prospectus.docx",
        ))
        for path in materials:
            with self.subTest(path=path.relative_to(ROOT)):
                content = docx_text(path) if path.suffix == ".docx" else path.read_text(encoding="utf-8")
                self.assertIn(CANONICAL_QUESTION.casefold(), " ".join(content.split()).casefold())

    def test_professor_materials_do_not_state_unsupported_metrics_as_results(self):
        materials = list(PROFESSOR_DOCS)
        materials.extend((
            ROOT / "academic-outreach/ThreatVision_One_Page_Research_Summary.docx",
            ROOT / "docs/research-prospectus.docx",
        ))
        for path in materials:
            with self.subTest(path=path.relative_to(ROOT)):
                content = docx_text(path) if path.suffix == ".docx" else path.read_text(encoding="utf-8")
                lowered = " ".join(content.split()).casefold()
                for claim in FORBIDDEN_CLAIMS:
                    self.assertNotIn(claim, lowered)
                unsupported_auc = "0.970 validation auc"
                if unsupported_auc in lowered:
                    position = lowered.index(unsupported_auc)
                    context = lowered[max(0, position - 40):position]
                    self.assertIn("unsupported", context)

    def test_historical_metric_mentions_are_locally_qualified(self):
        materials = list(PROFESSOR_DOCS)
        materials.extend((
            ROOT / "academic-outreach/ThreatVision_One_Page_Research_Summary.docx",
            ROOT / "docs/research-prospectus.docx",
        ))
        for path in materials:
            with self.subTest(path=path.relative_to(ROOT)):
                content = docx_text(path) if path.suffix == ".docx" else path.read_text(encoding="utf-8")
                lowered = " ".join(content.split()).casefold()
                for metric in HISTORICAL_METRICS:
                    start = 0
                    while True:
                        position = lowered.find(metric, start)
                        if position < 0:
                            break
                        context = lowered[max(0, position - 180):position + len(metric) + 180]
                        self.assertTrue(any(caveat in context for caveat in METRIC_CAVEATS),
                                        f"Unqualified historical metric {metric!r} in {path}")
                        start = position + len(metric)


if __name__ == "__main__":
    unittest.main()

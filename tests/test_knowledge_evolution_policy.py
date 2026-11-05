from pathlib import Path
import re
import unittest

SKILL = Path(__file__).resolve().parents[1] / 'skills' / 'knowledge-evolution' / 'SKILL.md'

class SkillPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.body = SKILL.read_text(encoding='utf-8')

    def test_frontmatter(self):
        self.assertTrue(self.body.startswith('---\n'))
        self.assertIn('\n---\n', self.body[4:])
        self.assertRegex(self.body, r'(?m)^name: knowledge-evolution$')
        self.assertRegex(self.body, r'(?m)^description: .+$')
        self.assertNotIn('TODO', self.body)

    def test_no_automatic_executable_promotion(self):
        self.assertIn('Do not auto-activate', self.body)
        self.assertIn('explicit authorization', self.body)
        self.assertIn('previous release', self.body)

    def test_negative_regression_transfer_coverage(self):
        for term in ['positive', 'negative', 'regression', 'transfer', 'rollback', 'independent']:
            self.assertIn(term, self.body.lower())

    def test_external_persistence_not_assumed(self):
        for status in ['PERSISTENCE_BLOCKED', 'PERSISTED_UNCOMMITTED', 'CANDIDATE_READY', 'ANALYSIS_ONLY']:
            self.assertIn(status, self.body)
        self.assertIn('Never say a Skill was installed', self.body)

    def test_paths_and_scheduling_guardrails(self):
        self.assertIn("never grants new access", self.body)
        self.assertIn("Never use `git add .`", self.body)

if __name__ == '__main__':
    unittest.main()

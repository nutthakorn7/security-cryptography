import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_forms  # noqa: E402
from forms_rule import ROOT, forms_for  # noqa: E402


class Rule(unittest.TestCase):
    def test_weeks_1_and_2_use_the_base_mapping(self):
        for w in (1, 2):
            self.assertEqual(forms_for(w), {"odd": "conventional", "even": "air-sec"})

    def test_even_weeks_keep_the_base_mapping(self):
        for w in (4, 6, 10, 12, 14):
            self.assertEqual(forms_for(w), {"odd": "conventional", "even": "air-sec"})

    def test_odd_weeks_from_3_are_flipped(self):
        for w in (3, 5, 11, 13, 15, 17):
            self.assertEqual(forms_for(w), {"odd": "air-sec", "even": "conventional"})

    def test_weeks_without_a_form_split(self):
        for w in (7, 8, 9):
            self.assertIsNone(forms_for(w))


class Detection(unittest.TestCase):
    def test_worksheet_line_matches(self):
        t = "**odd = AIR-Sec (Parts 3–4)**, **even = Conventional (Part 2)**"
        self.assertEqual(check_forms.check_text(t, 5, "x")[0], [])

    def test_worksheet_line_wrong(self):
        t = "**odd = Conventional (Part 2)**, **even = AIR-Sec (Parts 3–4)**"
        probs, found = check_forms.check_text(t, 5, "x")
        self.assertEqual(found, 1)
        self.assertEqual(len(probs), 1)

    def test_thai_line(self):
        t = "**เลขคี่ = AIR-Sec (Parts 3–4)**, **เลขคู่ = Conventional (Part 2)**"
        self.assertEqual(check_forms.check_text(t, 13, "x")[0], [])
        self.assertEqual(len(check_forms.check_text(t, 12, "x")[0]), 1)

    def test_slide_line(self):
        ok = "- **Your form (40):** student ID ends **odd** → AIR-Sec · **even** → Conventional"
        bad = "- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec"
        self.assertEqual(check_forms.check_text(ok, 3, "x")[0], [])
        self.assertEqual(len(check_forms.check_text(bad, 3, "x")[0]), 1)
        w1 = "student ID ends in an **odd** digit → Conventional · **even** → AIR-Sec"
        self.assertEqual(check_forms.check_text(w1, 1, "x")[0], [])

    def test_classroom_line(self):
        ok = "(attached below; odd ID = AIR-Sec sheet, even ID = Conventional sheet)"
        self.assertEqual(check_forms.check_text(ok, 11, "x")[0], [])
        self.assertEqual(len(check_forms.check_text(ok, 10, "x")[0]), 1)

    def test_parts_sentence(self):
        t = "Then do your own form: odd IDs do Parts 3 and 4; even IDs do Part 2."
        self.assertEqual(check_forms.check_text(t, 3, "x")[0], [])
        self.assertEqual(len(check_forms.check_text(t, 4, "x")[0]), 1)

    def test_statement_in_a_week_without_forms_is_reported(self):
        t = "**odd = Conventional (Part 2)**, **even = AIR-Sec (Parts 3–4)**"
        self.assertEqual(len(check_forms.check_text(t, 8, "x")[0]), 1)

    def test_submission_week_lists(self):
        good = "In Weeks 1, 2, 4 and 6 (and every even-numbered week) odd = Conventional and even = AIR-Sec; in Weeks 3,\n5 (every odd-numbered week from Week 3) odd = AIR-Sec"
        self.assertEqual(check_forms.check_general("SUBMISSION.md", good), [])
        bad = good.replace("Weeks 3,\n5", "Weeks 3,\n6")
        self.assertTrue(check_forms.check_general("SUBMISSION.md", bad))


class Repo(unittest.TestCase):
    def test_current_files_agree_with_forms_json(self):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "check_forms.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()

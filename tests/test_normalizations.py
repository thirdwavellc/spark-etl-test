import unittest
import nose  #For some lighter notations assert syntax   such as assert(fucn(x)) == 10
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.validations.validations import *
from models.normalizations.normalizations import *
from generate_objects import *


#Insert failed and passing values into the tests to make sure everything is working properly

class TestNormalizationsMethods(unittest.TestCase):

    def setUp(self):
        self.entries_true = list(map(lambda x: EligibilityEntry(x), panda_df('eligibility-false-tests.txt')))

    def test_normalize_coverage_start_date(self):
        normalize_coverage_start_date(self.entries_true[0],"coverage_start_date")
        self.assertEqual(valid_date_format(self.entries_true[0].coverage_start_date), True)

    def test_normalize_coverage_end_date(self):
        normalize_coverage_end_date(self.entries_true[0],"coverage_end_date")
        self.assertEqual(valid_date_format(self.entries_true[0].coverage_end_date), True)

    def test_normalize_date_of_birth(self):
        normalize_date_of_birth(self.entries_true[0],"date_of_birth")
        self.assertEqual(valid_dob(getattr(self.entries_true[0],"date_of_birth"),"date_of_birth").status,"passed")

    def test_normalize_first_name(self):
        normalize_first_name(self.entries_true[0],"first_name")
        self.assertEqual(valid_first_name(getattr(self.entries_true[0],"first_name"),"first_name").status,"passed")

    def test_normalize_last_name(self):
        normalize_last_name(self.entries_true[0],"last_name")
        self.assertEqual(valid_last_name(getattr(self.entries_true[0],"last_name"),"last_name").status,"passed")

    def test_normalize_email(self):
        normalize_email(self.entries_true[0],"email")
        self.assertEqual(valid_email(getattr(self.entries_true[0],"email"),"email").status,"passed")

    def test_normalize_zip(self):
        normalize_zip(self.entries_true[0],"zip_code")
        self.assertTrue(self.entries_true[0].zip_code == None or (valid_zip(getattr(self.entries_true[0],"zip_code"),"zip_code")).status =="passed")

    def test_normalize_state(self):
        normalize_state(self.entries_true[0],"state")
        self.assertEqual(valid_state(getattr(self.entries_true[0],"state"),"state").status,"passed")

if __name__ == '__main__':
    unittest.main()

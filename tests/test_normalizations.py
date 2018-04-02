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
        self.x = generate_objects_list("eligibility-false-tests.txt")


    def test_normalize_coverage_start_date(self):
        normalize_coverage_start_date(self.x.entries[0],"coverage_start_date")
        self.assertEqual(valid_date_format(self.x.entries[0].coverage_start_date), True)


    def test_normalize_coverage_end_date(self):
        normalize_coverage_end_date(self.x.entries[0],"coverage_end_date")
        print(valid_date_format(self.x.entries[0].coverage_end_date))
        self.assertEqual(valid_date_format(self.x.entries[0].coverage_end_date), True)


    def test_normalize_date_of_birth(self):
        normalize_date_of_birth(self.x.entries[0],"date_of_birth")
        self.assertEqual(valid_dob(self.x.entries[0],"date_of_birth").status,"passed")


    def test_normalize_first_name(self):
        normalize_first_name(self.x.entries[0],"first_name")
        self.assertEqual(valid_first_name(self.x.entries[0],"first_name").status,"passed")


    def test_normalize_last_name(self):
        normalize_last_name(self.x.entries[0],"last_name")
        self.assertEqual(valid_last_name(self.x.entries[0],"last_name").status,"passed")


    def test_normalize_email(self):
        normalize_email(self.x.entries[0],"email")
        self.assertEqual(valid_email(self.x.entries[0],"email").status,"passed")


    def test_normalize_zip(self):
        normalize_zip(self.x.entries[0],"zip_code")
        self.assertTrue(self.x.entries[0].zip_code == None or (valid_zip(self.x.entries[0],"zip_code")).status =="passed")


    def test_normalize_state(self):
        normalize_state(self.x.entries[0],"state")
        self.assertEqual(valid_state(self.x.entries[0],"state").status,"passed")





if __name__ == '__main__':
    unittest.main()

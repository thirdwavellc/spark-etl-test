import unittest
import nose  #For some lighter notations assert syntax   such as assert(fucn(x)) == 10
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.validations.validations import *
from models.schemas.radice import *
from generate_objects import *
import zipcodes



#Insert failed and passing values into the tests to make sure everything is working properly

class TestValidationMethods(unittest.TestCase):

    def setUp(self):
        self.entries_true = list(map(lambda x: EligibilityEntry(x), panda_df('eligibility-true-tests.txt')))
        self.entries_false = list(map(lambda x: EligibilityEntry(x), panda_df('eligibility-false-tests.txt')))


#Testing against incorrectly input data

    def test_valid_dob_bd(self):
        self.assertEqual(valid_dob(getattr(self.entries_false[0],"date_of_birth"),"date_of_birth").status, "failed")

    def test_valid_ssn_bd(self):
        self.assertEqual(valid_ssn(getattr(self.entries_false[0],"employee_ssn"),"employee_ssn").status,"failed")

    def test_valid_first_name_bd(self):
        self.assertEqual(valid_first_name(getattr(self.entries_false[0],"first_name"),"first_name").status,"failed")

    def test_valid_last_name_bd(self):
        self.assertEqual(valid_last_name(getattr(self.entries_false[0],"last_name"),"last_name").status,"failed")

    def test_valid_email_bd(self):
        self.assertEqual(valid_email(getattr(self.entries_false[0],"email"),"email").status,"failed")

    def test_valid_zip_bd(self):
        self.assertEqual(valid_zip(getattr(self.entries_false[0],"zip_code"),"zip_code").status, "failed")



#testing against correctly input data

    def test_valid_dob_gd(self):

        self.assertEqual(valid_dob(getattr(self.entries_true[0],"date_of_birth"),"date_of_birth").status, "passed")

    def test_valid_ssn_gd(self):

        self.assertEqual(valid_ssn(getattr(self.entries_true[0],"employee_ssn"),"employee_ssn").status,"passed")

    def test_valid_first_name_gd(self):
        self.assertEqual(valid_first_name(getattr(self.entries_true[0],"first_name"),"first_name").status,"passed")

    def test_valid_last_name_gd(self):
        self.assertEqual(valid_last_name(getattr(self.entries_true[0],"last_name"),"last_name").status,"passed")

    def test_valid_email_gd(self):
        self.assertEqual(valid_email(getattr(self.entries_true[0],"email"),"email").status,"passed")

    def test_valid_zip_gd(self):
        self.assertEqual(valid_zip(getattr(self.entries_true[0],"zip_code"),"zip_code").status, "passed")



if __name__ == '__main__':
    unittest.main()

import unittest
import nose  #For some lighter notations assert syntax   such as assert(fucn(x)) == 10
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.validations.validations import *
from generate_objects import *



#Insert failed and passing values into the tests to make sure everything is working properly

class TestValidationMethods(unittest.TestCase):


    def setUp(self):
        self.x = generate_objects_list("eligibility-false-tests.txt")
        self.y = generate_objects_list("eligibility-true-tests.txt")



#Testing against incorrectly input data

    def test_valid_dob_bd(self):

        self.assertEqual(valid_dob(self.x.entries[0],"date_of_birth").status, "failed")


    def test_valid_ssn_bd(self):
        self.assertEqual(valid_ssn(self.x.entries[0],"employee_ssn").status,"failed")


    def test_valid_first_name_bd(self):
        self.assertEqual(valid_first_name(self.x.entries[0],"first_name").status,"failed")


    def test_valid_last_name_bd(self):
        self.assertEqual(valid_last_name(self.x.entries[0],"last_name").status,"failed")


    def test_valid_email_bd(self):
        self.assertEqual(valid_email(self.x.entries[0],"email").status,"failed")

    def test_valid_zip_bd(self):
        self.assertEqual(valid_zip(self.x.entries[0],"zip_code").status, "failed")



#testing against correctly input data

    def test_valid_dob_gd(self):
        self.assertEqual(valid_dob(self.y.entries[0],"date_of_birth").status, "passed")


    def test_valid_ssn_gd(self):
        self.assertEqual(valid_ssn(self.y.entries[0],"employee_ssn").status,"passed")

    def test_valid_first_name_gd(self):
        self.assertEqual(valid_first_name(self.y.entries[0],"first_name").status,"passed")

    def test_valid_last_name_gd(self):
        self.assertEqual(valid_last_name(self.y.entries[0],"last_name").status,"passed")


    def test_valid_email_gd(self):
        self.assertEqual(valid_email(self.y.entries[0],"email").status,"passed")

    def test_valid_zip_gd(self):
        self.assertEqual(valid_zip(self.y.entries[0],"zip_code").status, "passed")




if __name__ == '__main__':
    unittest.main()

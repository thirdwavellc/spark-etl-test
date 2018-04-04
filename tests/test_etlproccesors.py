import unittest
import nose  #For some lighter notations assert syntax   such as assert(fucn(x)) == 10
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.validations.validations import *
from models.schemas.radice import *
from generate_objects import *



class TestEtlProcessors(unittest.TestCase):

    def setUp(self):
        self.objects_list = generate_objects_list('eligibility-sample.txt')

    def test_etl_base(self):



if __name__ == '__main__':
    unittest.main()

import os, sys
import time
from validate_email import validate_email
import datetime



#class Result:
#    def __init__(self, passed, error=""):
#        self.passed = passed
#        self.failed = not passed
#        self.error = error

class Validator:
    def __init__(self, entry, validations=[]):
        self.entry = entry
        self.validations = validations
        self.errors = ["first_name","last_name", "birth_date","email"]

#    def validate(self):
#        self._clear_errors()
#        self.validations = [valid_dob,valid_name]
#        validation_results = list(map(lambda validation: validation(self.entry), self.validations))
#        failed_validations = list(filter(lambda validation: validation.failed), validation_results)
#        self.errors = list(map(lambda validation: validation.error))
#        return len(self.errors) == 0

    def validate(self):
        self._clear_errors()
        validation_results = list(map(lambda validation: validation(self.entry), self.validations))
        self.errors = ["first_name","last_name", "birth_date","email"]
        failed_validations = [j for i, j in zip(validation_results, self.errors) if i == False]
        if (len(failed_validations) == 0):
            return True
        else:
            return failed_validations


    def _clear_errors(self):
        self.errors = []




def valid_dob(entry):
    try:
        #check that dob is in the right format
        valid_date = time.strptime(entry["date_of_birth"],'%Y%m%d')
        now = time.time()
        dob = (int(entry["date_of_birth"][0:4]),int(entry["date_of_birth"][4:6]),int(entry["date_of_birth"][6:8]),0,0,0,0,0,0)
        dob_to_seconds = time.mktime(dob)
        #make sure dob isn't in the future
        if dob_to_seconds<now:
            return(True)
        else:
            return(False)
    except ValueError:
        return(False)


def valid_ssn(entry):
    invalid_ssns = ["111111111", "222222222","333333333", "444444444", "555555555", "666666666","777777777",
            "888888888","999999999","123456789","987654321"]

    if (entry.ssn in invalid_ssns or entry.ssn!=9 or entry.ssn.isdigit()!=True):
        return(False)
    else:
        return(True)


def valid_first_name(entry):
    try:
        if(no_spaces(entry["first_name"]) and title_case(entry["first_name"]) and entry["first_name"].isalpha()):
            return(True)
        else:
            return(False)
    except:
        return(False)


def valid_last_name(entry):
    try:
        if(no_spaces(entry["last_name"]) and title_case(entry["last_name"]) and entry["last_name"].isalpha()):
            return(True)
        else:
            return(False)
    except:
        return(False)


def valid_email(entry):
        return((validate_email(entry["email"])))


#General functions
def no_spaces(string):
    if (' ' in string) == True:
        return(False)
    else:
        return(True)


def title_case(string):
    if (string.istitle()):
        return(True)
    else:
        return(False)


def test():
    entry={"first_name":"max","last_name":"Hansen","date_of_birth":"2017010","email":"mhansen1989@gmail.com"}

    validations = [valid_first_name,valid_last_name,valid_dob,valid_email]

    x = Validator(entry,validations)
    return x.validate()

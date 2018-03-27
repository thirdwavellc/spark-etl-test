import os, sys
import time
from validate_email import validate_email
import datetime

class ValidationResult:
    def __init__(self, entry, status, error=''):
        self.entry = entry
        self.status = status
        self.error = error

    def passed(self):
        self.status == 'passed'

    def failed(self):
        self.status == 'failed'

class Validator:
    def __init__(self, entry, validations=[]):
        self.entry = entry
        self.validations = validations
        self.errors = []

    def has_errors(self):
        return len(self.errors) > 0

    def validate(self):
        validation_results = list(map(lambda validation: validation(self.entry), self.validations))
        failed_validations = list(filter(lambda validation: validation.failed()), validation_results)
        self.errors = failed_validations
        return self

def no_validation(entry):
    return entry

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
        return ValidationResult(entry, 'failed', 'Invalid SSN')
    else:
        return ValidationResult(entry, 'passed')


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
        return((validate_email(entry["email"])) and no_spaces(entry["email"]))


#General functions
def no_spaces(field):
    if (' ' in field) == True:
        return(False)
    else:
        return(True)


def title_case(field):
    if (field.istitle()):
        return(True)
    else:
        return(False)


def is_greater_than(field,notgreaterthanthis):
    if len(field) > notgreaterthanthis:
        return(False)
    else:
        return(True)

def test():
    entry={"first_name":"max","last_name":"Hansen","date_of_birth":"2017010","email":"mhansen1989@gmail.com"}

    validations = [valid_first_name,valid_last_name,valid_dob,valid_email]

    x = Validator(entry,validations)
    return x.validate()

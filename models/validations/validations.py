import os, sys
import time
from validate_email import validate_email
import datetime
import zipcodes

class ValidationResult:
    def __init__(self, status,field_name, error=''):
        self.field_name = field_name
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
        return (len(self.errors) > 0)

    def validate(self):
        validation_results = list(map(lambda validation: validation[0](validation[1]), self.validations))
        failed_validations = list(filter(lambda validation: validation.status =="failed", validation_results))
        self.errors = list(map(lambda failed_validation: [failed_validation.field_name,getattr(self.entry,failed_validation.field_name),failed_validation.error],failed_validations))
        return self



def valid_dob(field_name):
    try:
        #check that dob is in the right format
        valid_date = time.strptime(field_name,'%Y%m%d')
        now = time.time()
        dob = (int(field_name[0:4]),int(field_name[4:6]),int(field_name[6:8]),0,0,0,0,0,0)
        dob_to_seconds = time.mktime(dob)
        #make sure dob isn't in the future
        if dob_to_seconds<now:
            return ValidationResult('passed',field_name)
        else:
            return ValidationResult( 'failed',field_name,'Your not from the future')
    except ValueError:
        return ValidationResult('failed',field_name, 'Wrong date format or invalid characters were used')


def valid_ssn(field_name):
    invalid_ssns = ["111111111", "222222222","333333333", "444444444", "555555555", "666666666","777777777",
            "888888888","999999999","123456789","987654321"]
    try:
        if (field_name in invalid_ssns or len(field_name)!=9 or field_name.isdigit()!=True):
            return ValidationResult( 'failed',field_name,  'Invalid SSN')
        else:
            return ValidationResult( 'passed',field_name)
    except:
        return ValidationResult('failed',field_name, 'Invalid SSN')


def valid_first_name(field_name):
    try:
        if(no_spaces(field_name) and title_case(field_name) and field_name.isalpha()):
            return ValidationResult('passed',field_name)
        else:
            return ValidationResult('failed',field_name,'Unexpected spacing, not title case or name contains non alphabetic characters')
    except:
        return ValidationResult( 'failed',field_name, 'Something went terribly wrong')


def valid_last_name(field_name):
    try:
        if(no_spaces(field_name) and title_case(field_name) and field_name.isalpha()):
            return ValidationResult('passed')
        else:
            return ValidationResult( 'failed',field_name, 'Unexpected spacing, not title case or name contains non alphabetic characters')
    except:
        return ValidationResult( 'failed',field_name, 'Something went terribly wrong')


def valid_email(field_name):
    if (validate_email(field_name) and no_spaces(field_name)):
        return ValidationResult( 'passed',field_name)

    else:
        return ValidationResult( 'failed',field_name,'invalid email')


def valid_zip(field_name):
    try:
        zip_code_normal = zipcodes.matching(getattr(entry,field_name))

        return ValidationResult('passed',field_name)
    except:
        return ValidationResult('failed',field_name)



def valid_state(field_name):
    attribute = getattr(entry,field_name)
    if(len(attribute)==2 and attribute.isupper()):
        return ValidationResult('passed',field_name)
    else:
        return ValidationResult('failed',field_name,'invalid state')


#General functions
def valid_date_format(date):
    print(date[0])
    if (len(date)==8 and date.isdigit() and (date[0]=="2" or date[0]=="1")):
        return True
    else:
        return False

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

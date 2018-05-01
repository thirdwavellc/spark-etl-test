"""Checks to see if the validator has any error from the entry"""
import os, sys
import time
from validate_email import validate_email
import datetime
import zipcodes

class ValidationResult:
    """The Validation result object is what is returned from the validation functionsselfself.
    The status is set to passed when the validation is passed and failed when the validation is failed."""
    def __init__(self, status,field_value,field_name, error=''):

        """
        Args:
            status = str
            field_value: str
            field_name: str
            error: str
        """
        self.field_value = field_value
        self.field_name = field_name
        self.status = status
        self.error = error

    def passed(self):
        """Sets the validation result object to passed.
        Args:
            None
        Returns:
            None
        """
        self.status == 'passed'

    def failed(self):
        """Sets the validation result object to failed.
        Args:
            None
        Returns:
            None
        """
        self.status == 'failed'

class Validator:
    """This object takes an custom entry object and an array of validation to perform on the entry"""
    def __init__(self, entry, entries, validations=[]):
        """

        Args:
            entry: Custom Entry Object (Ex.EligibilityEntry, CensusEntry)
            validations: array of validation functions
        """
        self.entry = entry
        self.entries = entries
        self.validations = validations
        self.errors = []

    def has_errors(self):
        """Checks to see if the validator has any error from the entry

        Args:
            None
        Returns:
            returns boolean
        """
        return (len(self.errors) > 0)

    def get_errors(self):
        """Returns array of errors

        Args:
            None
        Returns:
            returns array
        """
        return(self.errors)

    def validate(self):
        """Performs the validation on the entry object to check the validations assigned in the validation array

        Args:
            None
        Returns:
            returns self
        """
        validation_results = list(map(lambda validation: validation[0](getattr(self.entry,validation[1]),validation[1]), self.validations))
        orphan_validation = not_orphaned(self.entry,self.entries,self.entry.rel_to_subscriber)
        validation_results.append(orphan_validation)
        failed_validations = list(filter(lambda validation: validation.status =="failed", validation_results))
        self.errors =  list(map(lambda failed_validation: {"field_name":failed_validation.field_name,"field_value":failed_validation.field_value,"error":failed_validation.error},failed_validations))
        return self


def valid_dob(field_value,field_name):
    """Validates the date of birth by making sure it isn't in the future and that it is in the correct format of year month date (Ex. 20180102)

    Notes:
        Uses try to protect against failed inputs for the time.strptime function
    Args:
        field_value:str
        field_name:str
    Returns:
        returns Validation Result Object
    """
    try:
        #check that dob is in the right format
        valid_date = time.strptime(field_value,'%Y%m%d')
        now = time.time()
        dob = (int(field_value[0:4]),int(field_value[4:6]),int(field_value[6:8]),0,0,0,0,0,0)
        dob_to_seconds = time.mktime(dob)
        #make sure dob isn't in the future
        if dob_to_seconds<now:
            return ValidationResult('passed',field_value,field_name)
        else:
            return ValidationResult( 'failed',field_value,field_name,'Your not from the future')
    except ValueError:
        return ValidationResult('failed',field_value,field_name, 'Wrong date format or invalid characters were used')


def valid_ssn(field_value,field_name):
    """Validates the ssn by making sure it is 9 digits, is all digits and isnt part of the invalid ssn array

    Args:
        field_value:str
        field_name:str
    Returns:
        returns Validation Result Object
    """
    invalid_ssns = ["111111111", "222222222","333333333", "444444444", "555555555", "666666666","777777777",
            "888888888","999999999","123456789","987654321"]
    try:
        if (field_value in invalid_ssns or len(field_value)!=9 or field_value.isdigit()!=True):
            return ValidationResult( 'failed',field_value, field_name,  'Invalid SSN')
        else:
            return ValidationResult( 'passed',field_value,field_name)
    except:
        return ValidationResult('failed',field_value,field_name, 'Invalid SSN')


def valid_first_name(field_value,field_name):
    """Validates the first name by checking for empty spacing, making sure it's title case and that is only contains alpha characters

    Args:
        field_value:str
        field_name:str
    Returns:
        returns Validation Result Object
    """
    try:
        if(no_spaces(field_value) and title_case(field_value) and field_value.isalpha()):
            return ValidationResult('passed',field_value,field_name)
        else:
            return ValidationResult('failed',field_value,field_name,'Unexpected spacing, not title case or name contains non alphabetic characters')
    except:
        return ValidationResult( 'failed',field_value,field_name, 'Something went terribly wrong')


def valid_last_name(field_value,field_name):
    """Validates the last name by checking for empty spacing, making sure it's title case and that is only contains alpha characters

    Args:
        field_value:str
        field_name:str
    Returns:
        returns Validation Result Object
    """
    try:
        if(no_spaces(field_value) and title_case(field_value) and field_value.isalpha()):
            return ValidationResult('passed',field_value,field_name)
        else:
            return ValidationResult( 'failed',field_value,field_name, 'Unexpected spacing, not title case or name contains non alphabetic characters')
    except:
        return ValidationResult( 'failed',field_value,field_name, 'Something went terribly wrong')


def valid_email(field_value,field_name):
    """Validates the email by using the validate_email python library and checks that there are not spaces.

    Args:
        field_value:str
        field_name:str
    Returns:
        returns Validation Result Object
    """
    if (validate_email(field_value) and no_spaces(field_value)):
        return ValidationResult( 'passed',field_value,field_name)

    else:
        return ValidationResult( 'failed',field_value,field_name,'invalid email')


def valid_zip(field_value,field_name):
    """Validates the zip code by using the python zipcodes library.

    Args:
        field_value:str
        field_name:str
    Returns:
        returns Validation Result Object
    """
    try:
        zip_code_normal = zipcodes.matching(field_value)

        return ValidationResult('passed',field_value,field_name)
    except:
        return ValidationResult('failed',field_value,field_name)



def valid_state(field_value,field_name):
    """Validates the state by making sure it is only 2 characters in length and that both characters are alphabetic.

    Args:
        field_value:str
        field_name:str
    Returns:
        returns Validation Result Object
    """
    attribute = field_value
    if(len(attribute)==2 and attribute.isupper()):
        return ValidationResult('passed',field_value,field_name)
    else:
        return ValidationResult('failed',field_value,field_name,'invalid state')


def not_orphaned(entry, entries,rel_to_subscriber):
    """Checks to see of the entry has a parent subsciber. (Ex. a entry cannot be valid if they have a plan but no connecting member that works for the client company)

    Args:
        entry: Entry object
        entries: array of Entry objects
        rel_to_subscriber: str
    Returns:
        returns Validation Result Object
    """
    not_orphan=False
    for entry_other in entries:
        if ((entry.ins_subscriber_id == entry_other.ins_subscriber_id) and (entry_other.rel_to_subscriber =="0")):
            not_orphan=True
    if not_orphan:
        return ValidationResult('passed',rel_to_subscriber,'rel_to_subscriber')
    else:
        return ValidationResult('failed',rel_to_subscriber,'rel_to_subscriber','is orphan')




#General functions
def valid_date_format(date):
    """Validates a general date by making sure it is 8 digits long, are only digits and the year can only contain a 2 or 1 in the front (to exlude 0123,3000,4000)

    Args:
        date:str
    Returns:
        returns Boolean
    """
    if (len(date)==8 and date.isdigit() and (date[0]=="2" or date[0]=="1")):
        return True
    else:
        return False

def no_spaces(field):
    """Validates that there are no spaces in a string

    Args:
        field:str
    Returns:
        returns Boolean
    """
    if (' ' in field) == True:
        return(False)
    else:
        return(True)


def title_case(field):
    """Validates that as sting is title case
    Args:
        field:str
    Returns:
        returns Boolean
    """
    if (field.istitle()):
        return(True)
    else:
        return(False)


def is_greater_than(field,notgreaterthanthis):
    """Validates that a field length is not greater than the notgreaterthanthis value.

    Args:
        field:str
        notgreaterthanthis: int
    Returns:
        returns Boolean
    """
    if len(field) > notgreaterthanthis:
        return(False)
    else:
        return(True)

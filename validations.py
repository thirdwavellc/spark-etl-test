import os, sys

# import ../db.py
import time
from validate_email import validate_email




def valid_date(date):


    try:
        valid_date = time.strptime(date, '%m-%d-%Y')
    except ValueError:
        try:
            valid_date = time.strptime(date, '%m/%d/%Y')

        except ValueError:
            try:
                valid_date = time.strptime(date, '%m%d%Y')

            except ValueError:
                return(False)
    return(True)


def no_spaces(string):
    if (' ' in w) == True:
        return(False)
    else:
        return(True)


def title_case(string):
    if (string.istitle()):
        return(True)
    else:
        return(False)


def valid_ssn(ssn):
    invalid_ssns = ["111111111", "222222222","333333333", "444444444", "555555555", "666666666","777777777",
            "888888888","999999999","123456789","987654321"]

    if (ssn in invalid_ssns or ssn!=9 or ssn.isdigit()!=True):
        return(False)
    else:
        return(True)

def valid_email(email):
        return((validate_email(email))

def valid_zip(zipcode):
    try:
        zip_code_normal = zipcodes.matching(zip_code)
        return(True)
    except:

        return(None)










if __name__ == "__main__":
    main()

import os
import sys
from datetime import date
import math
import operator
import re
import zipcodes
import ast
import collections


class Normalizer:
    def __init__(self, entry, normalizations=[]):
        self.entry = entry
        self.normalizations = normalizations

    def normalize(self):
        list(map(lambda normalization: normalization[0](self.entry,normalization[1]), self.normalizations))


def normalize_coverage_start_date(entry,field_name):
    setattr(entry,field_name,normalize_date(getattr(entry,field_name)))


def normalize_coverage_end_date(entry,field_name):
    setattr(entry,field_name,normalize_date(getattr(entry,field_name)))


def normalize_date_of_birth(entry,field_name):
    setattr(entry,field_name,normalize_date(getattr(entry,field_name)))

#removes spaces and make name titlecase
def normalize_first_name(entry,field_name):
        spaces_removed_first_name = remove_spaces(getattr(entry,field_name))
        normalized_first_name = title_case(spaces_removed_first_name)
        setattr(entry,field_name,normalized_first_name)


#removes spaces, makes title case and removes and suffixes
def normalize_last_name(entry,field_name):
        spaces_removed_last_name = remove_spaces(getattr(entry,field_name))
        title_case_no_spaces = title_case(spaces_removed_last_name)
        normalized_last_name = remove_suffix(title_case_no_spaces)
        setattr(entry,field_name, normalized_last_name)

#removes spaces from the email
def normalize_email(entry,field_name):
    setattr(entry,field_name,remove_spaces(getattr(entry,field_name)))


#utilizes the zipcodes python lib that returns a dictionary. One of the items is a 5 digit zip. Even if user inputs longer zip version it will return 5 digit zip
def normalize_zip(entry,field_name):
        try:
                zip_code_normal = zipcodes.matching(getattr(entry,field_name))[0]['zip_code']
                setattr(entry,field_name,zip_code_normal)
        except:
                setattr(entry,field_name,None)

def phone_strip_nondigits(entry,field_name):
    setattr(entry,field_name,re.sub('[^0-9]','', getattr(entry,field_name)))

def normalize_state(entry,field_name):
    try:
        setattr(entry,field_name,getattr(entry,field_name).upper())
    except:
        setattr(entry,field_name, None)




#Generic Functions

def normalize_date(date):
        whitelist = set('0123456789')
        normalized_date = ''.join(filter(whitelist.__contains__, date))

        return(str(normalized_date))

def remove_spaces(string):
        string = string.replace(" ", "")
        return str(string)

def title_case(string):
         string = string.lower().title()
         return string

def remove_suffix(string):
          suffixes = ["Esq", "Ii", "Iii", "Iiii", "Iv", "Jnr", "Jr", "Sr"]
          string = string.replace(" ", "")
          string = string.replace(".", "")
          string = string.replace(",", "")
          for suffix in suffixes:
                  if(string.endswith(suffix)):
                          string = string[:-len(suffix)]
                          return(string)
          return(string)

#def clean_ssn():

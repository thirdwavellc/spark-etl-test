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
        list(map(lambda normalization: normalization(self.entry), self.normalizations))


#only allow numbers within the date (auto removes anything but numbers)
def normalize_date(date):
	whitelist = set('0123456789')
	normalized_date = ''.join(filter(whitelist.__contains__, date))

	return(str(normalized_date))

def normalize_date_of_birth(entry):
    entry.date_of_birth = normalize_date(entry.date_of_birth)

#removes spaces and make name titlecase
def normalize_first_name(string):
	spaces_removed_first_name = remove_spaces(string)
	normalized_first_name = title_case(spaces_removed_first_name)
	return(normalized_first_name)

def normalize_first_name(string):
	string = remove_spaces(string)
	string = title_case(string)
	return string

#removes spaces, makes title case and removes and suffixes
def normalize_last_name(string):
	spaces_removed_last_name = remove_spaces(string)
	title_case_no_spaces = title_case(spaces_removed_last_name)
	normalized_last_name = remove_suffix(title_case_no_spaces)
	return(normalized_last_name)

#removes spaces from the email
def normalize_email(string):
	return(remove_spaces(string))

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

#utilizes the zipcodes python lib that returns a dictionary. One of the items is a 5 digit zip. Even if user inputs longer zip version it will return 5 digit zip
def normalize_zip(zip_code):
	try:
		zip_code_normal = zipcodes.matching(zip_code)[0]['zip_code']
		return(str(zip_code_normal))
	except:
		return(None)

def phone_strip_nondigits(phone):
	return(re.sub('[^0-9]','', phone))

def uppercase_state(state):
	try:
		return(state.upper())
	except:
		return(None)

def uppcase_state(state):
	return(state.upper())


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

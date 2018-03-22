import os
import sys
from datetime import date
import math
import operator
import re
import zipcodes
import ast


class customRow:

	def __init__(self, row_object,eligibility_schema):
		self.dictionary={}
		for field in eligibility_schema:
			self.dictionary[field.name] = row_object[field.name]


	def to_array(self,fields):
		new_array=[]
		for i in fields:
			new_array.append(self.dictionary[i.name])
		return(new_array)















def normalize_first_name(string):
	string = remove_spaces(string)
	string = title_case(string)
	return(string)

def normalize_last_name(string):
	string = remove_spaces(string)
	string = title_case(string)
	string = remove_suffix(string)
	return string

def normalize_email(string):
	return(remove_spaces(string))


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

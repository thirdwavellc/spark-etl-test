import os
import sys
from datetime import date
import math
import operator
import re
import zipcodes
import ast



def normalize_list(list_object,schema_names):
	 var_to_normalize=["first_name","last_name","email","zip_code"]
	 new_list=[None]*len(list_object)
	 index_first_name = schema_names.index("first_name")
	 index_last_name = schema_names.index("last_name")
	 index_email = schema_names.index("email")
	 index_zip = schema_names.index("zip_code")
	 new_list[index_first_name]=normalize_first_name(list_object[index_first_name])
	 new_list[index_last_name]=normalize_last_name(list_object[index_last_name])
	 new_list[index_email]=normalize_email(list_object[index_email])
	 new_list[index_zip]=normalize_zip(list_object[index_zip])
	 for name in schema_names:
		 if (name not in var_to_normalize):
			 print(name)
			 new_list[schema_names.index(name)]= list_object[schema_names.index(name)]
	 return(new_list)




def normalize_first_name(string):
	string = remove_spaces(string)
	string = title_case(string)
	return string

def normalize_last_name(string):
	string = remove_spaces(string)
	string = title_case(string)
	string = remove_suffix(string)
	return string

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


def normalize_zip(zip_code):
	print("here")
	print(zip_code)
	try:
		print("success")
		zip_code_normal = zipcodes.matching(zip_code)[0]['zip_code']
		return(str(zip_code_normal))
	except:

		return(None)

def phone_strip_nondigits(phone):
	return(re.sub('[^0-9]','', phone))


def uppcase_state(state):
	return(state.upper())


def remove_spaces(string):
	 string = string.replace(" ", "")
 	 return str(string)

def title_case(string):
	 string = string.lower().title()
 	 return string



#def clean_ssn():

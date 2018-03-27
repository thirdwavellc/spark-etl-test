import os
import sys
from datetime import date
import math
import operator
import re
import zipcodes
import ast
import collections


class customRow:

	def __init__(self, row_object,eligibility_schema):

		#created a variable for each field just for backup for now (was thinking of removing these and just using a single dictionary for easier customization for individual clients)
		self.source_id = row_object["source_id"]
		self.client_name = row_object["client_name"]
		self.field = row_object["field"]
		self.run_date = row_object["run_date"]
		self.employee_ssn = row_object["employee_ssn"]
		self.member_ssn = row_object["member_ssn"]
		self.rel_to_subscriber = row_object["rel_to_subscriber"]
		self.last_name = row_object["last_name"]
		self.first_name = row_object["first_name"]
		self.date_of_birth = row_object["date_of_birth"]
		self.gender =row_object["gender"]
		self.benefit_type = row_object["benefit_type"]
		self.coverage_level = row_object["coverage_level"]
		self.group_number= row_object["group_number"]
		self.ins_subscriber_id = row_object["ins_subscriber_id"]
		self.member_id = row_object["member_id"]
		self.plan_id  = row_object["plan_id"]
		self.plan_name = row_object["plan_name"]
		self.coverage_status = row_object["coverage_status"]
		self.email = row_object["email"]
		self.address_line_1 = row_object["address_line_1"]
		self.address_line_2 = row_object["address_line_2"]
		self.city=row_object["city"]
		self.state = row_object["state"]
		self.zip_code =row_object["zip_code"]


		#create a dictionary to store the fields of the eligibility_schema
		#this way seems like it will be easier than doing as I did above in creating a variable for each field
		self.dictionary=collections.OrderedDict()
		for field in eligibility_schema:
			self.dictionary[field.name] = str(row_object[field.name])


	#Returns an array of the dictionary if needed.
	def to_array(self,fields):
		new_array=[]
		for i in fields:
			new_array.append(self.dictionary[i.name])
		return(new_array)






def normalize_list(entry,schema_names):
	 var_to_normalize=["first_name","last_name","zip_code","date_of_birth"]
	 new_list=[None]*len(entry.dictionary)
	# index_first_name = schema_names.index("first_name")
	# index_last_name = schema_names.index("last_name")
	 #index_email = schema_names.index("email")
	# index_zip = schema_names.index("zip_code")
	# index_dob = schema_names.index("date_of_birth")

	# new_list[index_first_name]=normalize_first_name(entry.dictionary["first_name"])
	# new_list[index_last_name]=normalize_last_name(entry.dictionary["last_name"])
	# new_list[index_email]=normalize_email(entry.dictionary["email"])
	# new_list[index_zip]=normalize_zip(entry.dictionary["zip_code"])
	# new_list[index_dob]=normalize_date(entry.dictionary["date_of_birth"])


	 entry.dictionary["first_name"] = normalize_first_name(entry.dictionary["first_name"])
	 entry.dictionary["last_name"] = normalize_last_name(entry.dictionary["last_name"])
	# entry.dictionary["email"] = normalize_last_name(entry.dictionary["email"])
	 entry.dictionary["zip_code"] = normalize_zip(entry.dictionary["zip_code"])
	 entry.dictionary["date_of_birth"] = normalize_date(entry.dictionary["date_of_birth"])

	# for name in schema_names:
		# if (name not in var_to_normalize):
			 #new_list[schema_names.index(name)]= str(entry.dictionary[name])
			 #entry.dictionary[name] = entry.dictionary[name]
	 return(entry.dictionary)

#only allow numbers within the date (auto removes anything but numbers)
def normalize_date(date):
	whitelist = set('0123456789')
	normalized_date = ''.join(filter(whitelist.__contains__, date))

	return(str(normalized_date))

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

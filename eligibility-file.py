'''Converts sample Eligibilty file into JSON'''
import os
from datetime import date
import math
import operator
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType, StringType
import csv
import json
import sys, getopt
import pandas
import re
import sys
import normalize
import ipdb;

def main():

    spark = SparkSession\
        .builder\
        .appName("PySparkEligibiltyFile")\
        .getOrCreate()

    df = spark.read \
        .format("CSV") \
        .schema(eligibility_schema()) \
        .option("header", "false") \
        .option("delimiter", "|") \
        .option("treatEmptyValuesAsNulls", "true") \
        .load(data_file())

    data_frame_object = df.collect()

    #Possible array for the normalization functions
    normalize_functions=[]

    #Create a new list to insert our custom row objects into
    custom_row_list = []

    #Loop thought the data frame object and go through each row
    for i in range(0,len(data_frame_object)):

        spark_row_object = data_frame_object[i]

        #Create a new Custom Row Object using
        cr=normalize.customRow(spark_row_object,eligibility_schema())


        #Normalizing data
        cr.dictionary['first_name'] = normalize.normalize_first_name(cr.dictionary['first_name'])
        cr.dictionary['last_name'] = normalize.normalize_last_name(cr.dictionary['last_name'])
        cr.dictionary['email'] = normalize.normalize_email(cr.dictionary['email'])
        cr.dictionary['state'] = normalize.uppercase_state(cr.dictionary['state'])
        cr.dictionary['date_of_birth'] = normalize.normalize_date(cr.dictionary['date_of_birth'])


        #This will put the object into an array version
        #array_version=cr.to_array(eligibility_schema())

        custom_row_list.append(cr.dictionary)



        #Validate the normalized data
        validate_object = Validator(cr,[valid_name,valid_dob])




    #TO-DO Code something that creates a folder instead of relying on already having that folder there

    i = 0
    while i < len(custom_row_list):
        with open('jsonfiles/data'+str(i)+'.json', 'w') as f:
            json.dump(custom_row_list[i:i+100], f)
        i += 100




def eligibility_schema():
    '''Defines schema in Eligibility file for CSV ingestion (assuming no header present)'''
    return StructType([
        StructField('source_id', StringType()),         #No validation
        StructField('client_name', StringType()),       #No validation
        StructField('field', StringType()),             #No validation
        StructField('run_date', StringType()),          #Yes validation
        StructField('employee_ssn', StringType()),      #Yes validation
        StructField('member_ssn', StringType()),        #Yes validation
        StructField('rel_to_subscriber', StringType()), #No validation
        StructField('last_name', StringType()),         #Yes validation
        StructField('first_name', StringType()),        #Yes validation
        StructField('date_of_birth', StringType()),     #Yes validation
        StructField('gender', StringType()),            #No validation
        StructField('benefit_type', StringType()),      #No validation
        StructField('coverage_level', StringType()),    #Yes validation
        StructField('group_number', StringType()),      #No validation
        StructField('ins_subscriber_id', StringType()), #No validation
        StructField('member_id', StringType()),         #No validation
        StructField('plan_id', StringType()),           #No validation
        StructField('plan_name', StringType()),         #No validation
        StructField('coverage_start_date', StringType()), #Yes validation
        StructField('coverage_end_date', StringType()),   #Yes validation
        StructField('coverage_status', StringType()),     #No validation
        StructField('email', StringType()),             #Yes validation
        StructField('address_line_1', StringType()),    #No validation
        StructField('address_line_2', StringType()),    #No validation
        StructField('city', StringType()),              #No validation
        StructField('state', StringType()),             #No validation
        StructField('zip_code', StringType())           #Yes validation
    ])


def data_file():
    '''Path that contains sample Eligibility file'''
    file_dir = os.path.dirname(__file__)
    return os.path.join(file_dir,  "eligibility-sample.txt")

def saved_text_file():
    '''Filename for saved text file'''
    datestamp = date.today().strftime("%Y%m%d")
    return "eligibility-sample-" + datestamp






if __name__ == "__main__":
    main()

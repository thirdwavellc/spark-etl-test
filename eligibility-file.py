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
import ipdb;
import eligibility_file.eligibility_file.validations as v
import eligibility_file.eligibility_file.models as m
import eligibility_file.eligibility_file.normalizations as n
import eligibility_file.eligibility_file

# TODO: move into library
#def create_spark_session(app_name):
#    spark = SparkSession\
#       .builder\
#       .appName(app_name)\
#       .getOrCreate()
#    return spark

# TODO: move into library
def get_data_frame_list(schema, data_file,app_name):
    spark = SparkSession\
           .builder\
           .appName(app_name)\
           .getOrCreate()

    return spark.read \
        .format("CSV") \
        .schema(schema) \
        .option("header", "false") \
        .option("delimiter", "|") \
        .option("treatEmptyValuesAsNulls", "true") \
        .load(data_file) \
        .collect()

# TODO: move into client-specific file
class RadiceEtlProcessor:
    def __init__(self):
        #self.spark = create_spark_session("PySparkEligibiltyFile")
        self.data_frame_list = get_data_frame_list(self.eligibility_schema(), self.data_file(),"PySparkEligibiltyFile")
        self.entries = self.create_entries()
        self.normalizations = [
        n.normalize_date_of_birth,
        n.normalize_coverage_start_date,
        n.normalize_coverage_end_date,
        n.normalize_first_name,
        n.normalize_last_name,
        n.normalize_email,
        n.normalize_zip,
        n.normalize_state]

        self.validations = [
        v.valid_dob,
        v.valid_ssn,
        v.valid_first_name,
        v.valid_last_name,
        v.valid_email
        ]

    def process(self):
        self.normalize()
        self.validate()
        self.export()

    def create_entries(self):
        return list(map(lambda data_frame: m.Entry(data_frame, self.eligibility_schema()), self.data_frame_list))

    def normalize(self):
        list(map(lambda entry: n.Normalizer(entry, self.normalizations).normalize(), self.entries))


    def validate(self):
        self.validators = list(map(lambda entry: v.Validator(entry, self.validations).validate(), self.entries))
        self.valid_validators = filter(lambda validator: not validator.has_errors(), self.validators)
        self.invalid_validators = filter(lambda validator: validator.has_errors(), self.validators)



    def return_fields(self,validator):
        valid_entry_array =[]
        for attr, value in validator.entry.__dict__.items():
            valid_entry_array.append(value)
        return valid_entry_array

    def export(self):

        valid_entries_array= list(map(lambda validator:self.return_fields(validator),self.valid_validators))
        invalid_entries_array= list(map(lambda validator:self.return_fields(validator),self.valid_validators))


        i = 0
        while i < len(valid_entries_array):
            with open('passedentries/data'+str(i)+'.json', 'w') as f:
                json.dump(valid_entries_array[i:i+100], f)
            i += 100

        i = 0
        while i < len(invalid_entries_array):
            with open('failedentries/data'+str(i)+'.json', 'w') as f:
                json.dump(invalid_entries_array[i:i+100], f)
            i += 100




    def eligibility_schema(self):
        '''Defines schema in Eligibility file for CSV ingestion (assuming no header present)'''
        return StructType([
            StructField('source_id', StringType()),         #No validation
            StructField('client_name', StringType()),       #No validation
            StructField('field', StringType()),             #No validation
            StructField('run_date', StringType()),          #Yes validation
            StructField('employee_ssn', StringType()),          #Yes validation
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

    def data_file(self):
        '''Path that contains sample Eligibility file'''
        file_dir = os.path.dirname(__file__)
        return os.path.join(file_dir,  "eligibility-sample.txt")



def main():
    etl_process = RadiceEtlProcessor()
    etl_process.process()




def saved_text_file():
    '''Filename for saved text file'''
    datestamp = date.today().strftime("%Y%m%d")
    return "eligibility-sample-" + datestamp






if __name__ == "__main__":
    main()

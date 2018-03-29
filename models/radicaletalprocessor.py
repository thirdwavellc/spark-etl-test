import os
from datetime import date
import math
import operator
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import csv
import json
import sys
import paramiko
import validations.validations as valid
import entry as entry
import normalizations.normalizations as norm
import etlprocessor as etlprocessor
import pandas

def get_file_from_sftp(key_path,username):
    p_key = paramiko.RSAKey.from_private_key_file(key_path)
    con = paramiko.SSHClient()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect( hostname = "ec2-34-206-40-147.compute-1.amazonaws.com", username = username, pkey = p_key )
    sftp_con = con.open_sftp()
    return (sftp_con.open('/uploads/radice/eligibility-sample.txt'))




# TODO: move into library
def get_data_frame_list(schema,app_name):
    spark = SparkSession\
           .builder\
           .appName(app_name)\
           .getOrCreate()

    data = pandas.read_csv(get_file_from_sftp('/home/max/Downloads/radice-sftp.pem','radice'),sep='|',header=0)
    return((spark.createDataFrame(data,schema)).collect())


class RadiceEtlProcessor(etlprocessor.EtlProcessor):
    def __init__(self):
        self.data_frame_list = get_data_frame_list(self.eligibility_schema(),"PySparkEligibiltyFile")
        self.entries = self.create_entries()
        self.normalizations = [
        norm.normalize_date_of_birth,
        norm.normalize_coverage_start_date,
        norm.normalize_coverage_end_date,
        norm.normalize_first_name,
        norm.normalize_last_name,
        norm.normalize_email,
        norm.normalize_zip,
        norm.normalize_state]

        self.validations = [
        valid.valid_dob,
        valid.valid_ssn,
        valid.valid_first_name,
        valid.valid_last_name,
        valid.valid_email
        ]


    def export(self):

        valid_entries_dic= list(map(lambda validator:self.return_fields(validator),self.valid_validators))
        invalid_entries_dic= list(map(lambda validator:self.return_fields(validator),self.invalid_validators))

        self.file_partition_size(valid_entries_dic,1000000,'json/clienta/passedentries')
        self.file_partition_size(invalid_entries_dic,1000000,'json/clienta/failedentries')


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
        return os.path.join(file_dir,  "../eligibility-sample.txt")

    def downloaded_data_file(self):
        '''Path that contains sample Eligibility file'''
        file_dir = os.path.dirname(__file__)
        return os.path.join(file_dir,  "../sftpserverdls/eligibility-sample-copy.txt")

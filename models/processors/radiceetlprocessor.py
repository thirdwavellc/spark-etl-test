
from pyspark.sql.types import *
from ..validations import validations as valid
from ..normalizations import normalizations as norm
import etlprocessor as etlprocessor
from .. import helpfunctions as helper
from ..entries import radiceentry as radiceentry


class RadiceEtlProcessor(etlprocessor.EtlProcessor):
    def __init__(self):
        self.data_frame_list = helper.get_data_frame_list(self.eligibility_schema(),"PySparkEligibiltyFile")
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

    def create_entries(self):
        return list(map(lambda data_frame: radiceentry.RadiceEntry(data_frame, self.eligibility_schema()), self.data_frame_list))

    def export(self):

        valid_entries_dic= list(map(lambda validator:self.return_fields(validator),self.valid_validators))
        invalid_entries_dic= list(map(lambda validator:self.return_fields(validator),self.invalid_validators))
        helper.file_partition_size(valid_entries_dic,1000000,'json/radice/passedentries')
        helper.file_partition_size(invalid_entries_dic,1000000,'json/radice/failedentries')

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

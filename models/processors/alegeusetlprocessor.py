
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import validations.validations as valid
import entries.alegusentry as alegeusentry
import normalizations.normalizations as norm
import etlprocessor as etlprocessor
import helpfunctions as helper



class AlegeusEtlProcessor(etlprocessor.EtlProcessor):
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
        return list(map(lambda data_frame: radiceentry.AlegeusEntry(data_frame, self.eligibility_schema()), self.data_frame_list))


    def export(self):
        valid_entries_dic= list(map(lambda validator:self.return_fields(validator),self.valid_validators))
        invalid_entries_dic= list(map(lambda validator:self.return_fields(validator),self.invalid_validators))

        self.file_partition_size(valid_entries_dic,1000000,'json/alegeus/passedentries')
        self.file_partition_size(invalid_entries_dic,1000000,'json/alegeus/failedentries')

    def eligibility_schema(self):
        '''Defines schema in Eligibility file for CSV ingestion (assuming no header present)'''
        return StructType([
            StructField('record_header', StringType()),         #Len 2    Value = FE                                           #Required
            StructField('tpa_id', StringType()),                #Len 6    Value = Unique Identifier that WCA assigns to you    #Required
            StructField('employer_id', StringType()),           #Len 9-12 Value = Unique identifier for the employer. WCA assigns the 3-character prefix; you assign the next 6 characters.  #Required
            StructField('employee_id', StringType()),           #Len 9-30 Value = Unique Identifier for employee               #Required
            StructField('last_name', StringType()),             #Len 26  #Required #WCA verifies that only allowable characters are entered. Illegal characters are ones that cannot be printed on the Benefits Cards.
            StructField('first_name ', StringType()),           #Len 19  #Required DIDO
            StructField('prefix', StringType()),                #Len 5
            StructField('middle_initial', StringType()),        #Len 1
            StructField('phone', StringType()),                 #Len 19  Employee’s phone number,including area code.Note: Spaces for an extension can be left blank, if appropriate.
            StructField('address_line_1', StringType()),        #Len 36-75
            StructField('address_line_2', StringType()),        #Len 36-75
            StructField('city', StringType()),                  #Len 20-30
            StructField('state', StringType()),                 #Two-character state code associated with the employee’s address.
            StructField('zip_code', StringType())               #Len 9-15   Note: For employees with Product Partner HSA accounts,this field must be 9 or fewer characters.
            StructField('country', StringType()),               #Len 3  The allowable values are US, or US followed by a blank, if you use fixed length fields.
            StructField('email', StringType()),
            StructField('gender', StringType()),                #Len 1   0 = Unknown  1 = Male  2 = Female
            StructField('maritial_status', StringType()),       #Len 1  0 = Unknown 1 = Single 2 = Married 3 = Separated 4 = Widowed 5 = Divorced
            StructField('birth_date', StringType()),            #Len 8  YYYYMMDD  Date of birth for the employee. Note: This information is required by Product Partners if Employee will be set up with an HSM or HSB account.
            StructField('employee_social_security_number', StringType()),      #Len 9 Note 1: You can use this field for TPS matching or to search for an employee using the advanced search feature in the
# UI. Note 2: This information is required by Product Partners if Employee will be set up with a Product Partner HSA account.
            StructField('hdhp_eligible', StringType()),      #Len 1 lag indicating whether the employee is eligible for an High Deductible Health Plan 0 = No 1 = Yes
# Note: When used in conjunction with a Product Partner, which requires eligibility match, the employee will not be included in the HSA Product Partner Eligibility file unless this value is
# set to YES. The default value for this field is NO.
            StructField('drivers_license_number', StringType()), #Len 20
            StructField('mothers_maiden_name', StringType()),
            StructField('base_salary', StringType()),
            StructField('eligibility_date', StringType()),         #Len 8 Date upon which the employee is eligible to elect benefits. This existing field is being updated
        #    to validate that it is prior to the termination date.
            StructField('original_hire_date', StringType()), #Len 8
            StructField('employment_type', StringType()),   #Len 1   The employee’s type of employment: 1 = Full Time (default) 2 = Part Time 3 = Contract
            StructField('division', StringType()),     #Len 50
            StructField('employee_citizenship_status', StringType()),  #Len 1
            StructField('class', StringType()), #Len 50
            StructField('record_tracking_number', StringType()),   #len 20
            StructField('wealthcare_marketplace_employee_id', StringType()), #Len 36 Max Len 36 Alpahnumeric

        ])

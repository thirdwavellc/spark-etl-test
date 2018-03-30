from pyspark.sql.types import *

eligibility_file = StructType([
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

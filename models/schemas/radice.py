from pyspark.sql.types import *


"""This is a spark StructType obect that stores the field names for the client"""

eligibility_file = StructType([
    StructField('source_id', StringType()),
    StructField('client_name', StringType()),
    StructField('field', StringType()),
    StructField('run_date', StringType()),
    StructField('employee_ssn', StringType()),
    StructField('member_ssn', StringType()),
    StructField('rel_to_subscriber', StringType()),
    StructField('last_name', StringType()),
    StructField('first_name', StringType()),
    StructField('date_of_birth', StringType()),
    StructField('gender', StringType()),
    StructField('benefit_type', StringType()),
    StructField('coverage_level', StringType()),
    StructField('group_number', StringType()),
    StructField('ins_subscriber_id', StringType()),
    StructField('member_id', StringType()),
    StructField('plan_id', StringType()),
    StructField('plan_name', StringType()),
    StructField('coverage_start_date', StringType()),
    StructField('coverage_end_date', StringType()),
    StructField('coverage_status', StringType()),
    StructField('email', StringType()),
    StructField('address_line_1', StringType()),
    StructField('address_line_2', StringType()),
    StructField('city', StringType()),
    StructField('state', StringType()),
    StructField('zip_code', StringType())
])

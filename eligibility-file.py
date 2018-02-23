'''Converts sample Eligibilty file into JSON'''
import os
from datetime import date
import math
import operator
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType, StringType

def main():
    '''Program entry point'''

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

    partitions = int(math.ceil(df.count() / 100))
    df_of_json = df.repartition(partitions).toJSON(use_unicode=True)
    df_of_json.saveAsTextFile(saved_text_file())

def eligibility_schema():
    '''Defines schema in Eligibility file for CSV ingestion (assuming no header present)'''
    return StructType([
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

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
#change



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


#    sc = spark.sparkContext

    # Load a text file and convert each line to a Row.
#    lines = sc.textFile(data_file())
#    parts = lines.map(lambda l: l.split("|"))
    # Each line is converted to a tuple.
#    people = parts.map(lambda p: (p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11],p[12],p[13],p[14],p[15],
#    p[16],p[17],p[18],p[19],p[20],p[21],p[22],p[23],p[24],p[25],p[26].strip()))

    # The schema is encoded in a string.
#    schemaString = "source_id client_name field run_date employee_ssn member_ssn rel_to_subscriber last_name first_name date_of_birth gender benefit_type coverage_level group_number ins_subscriber_id member_id plan_id plan_name coverage_start_date coverage_end_date coverage_status email address_line_1 address_line_2 city state zip_code"


#    fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
#    schema = StructType(fields)

    # Apply the schema to the RDD.
#    schemaPeople = spark.createDataFrame(people, schema)

    # Creates a temporary view using the DataFrame
    #schemaPeople.createOrReplaceTempView("people")
#    results = spark.sql("SELECT * FROM people")

    #query_string = "SELECT * FROM people"
    #results = spark.sql(query_string)



    val_list = df.collect()
    json.dumps(val_list)
    with open('data.txt', 'w') as outfile:
        json.dump(val_list, outfile)


    i = 0
    while i < len(val_list):
        with open('jsonfiles/data'+str(i)+'.json', 'w') as f:
            json.dump(val_list[i:i+100], f)
        i += 100

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

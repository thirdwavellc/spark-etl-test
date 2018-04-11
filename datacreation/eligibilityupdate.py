
from datetime import date
import math
import operator
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType, StringType
import csv
import json
import getopt
import pandas
import re
import random
from faker import Faker
import numpy as np
import os, sys
fake = Faker()
import eligibility_file_generator as fg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.schemas.radice import eligibility_file



def random_delete_entry(input_file):
    spark = SparkSession\
        .builder\
        .appName("PySparkEligibiltyFile")\
        .getOrCreate()

    df = self.spark_session.read \
                    .format("CSV") \
                    .schema(eligibility_file) \
                    .option("header", "false") \
                    .option("delimiter", "|") \
                    .option("treatEmptyValuesAsNulls", "true") \
                    .load(input_file) \






def random_file_update(input_file):
    updated_attributes = {"last_name": fake.last_name() ,"first_name": fake.first_name() ,"email": fake.email(), "city": fake.city(), "state": fake.state(), "zip_code": fg.add_alpha_char(50,fake.zipcode()),
     "address_line_1": fake.street_address(),}
    updated_attributes_array = ["last_name","first_name","email","city","state","zip_code","address_line_1"]

    spark_session = SparkSession\
        .builder\
        .appName("PySparkEligibiltyFile")\
        .getOrCreate()

    df = spark_session.read \
                    .format("CSV") \
                    .schema(eligibility_file) \
                    .option("header", "false") \
                    .option("delimiter", "|") \
                    .option("treatEmptyValuesAsNulls", "true") \
                    .load(input_file) \




    rows = df.collect()
    for row in rows:
        random_attribute = np.random.choice(updated_attributes_array)
        random_chance = random.randint(1, 100)
        if random_chance<=100:
            if(row[random_attribute]!= None):

                df2 = df.na.replace(row[random_attribute],updated_attributes[random_attribute],random_attribute)


    df2.write.csv("csv",sep="|")




if __name__ == "__main__":
    random_file_update("/home/max/Work/thirdwave/zest/sparketl/spark-etl-test/datacreation/eligibility-sample.txt")

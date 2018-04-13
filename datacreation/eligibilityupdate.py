
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
#import eligibility_file_generator as fg

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
    updated_attributes = {"last_name": fake.last_name() ,"first_name": fake.first_name() ,"email": fake.email(), "city": fake.city(), "state": fake.state(), "zip_code": fake.zipcode(),
     "address_line_1": fake.street_address(),}
    updated_attributes_array = ["last_name","first_name","email","city","state","zip_code","address_line_1"]
    df = pandas.DataFrame(pandas.read_csv("eligibility-sample.txt",sep="|",header=None,names=eligibility_file.fieldNames(),dtype=str))
    for index, row in df.iterrows():
        random_attribute = np.random.choice(updated_attributes_array)
        random_chance = random.randint(1, 100)
        if random_chance<=100:
            df.loc[index,random_attribute]=updated_attributes[random_attribute]




    df.to_csv('transformed-test-data.txt',header=None,sep="|",index=False)




if __name__ == "__main__":
    random_file_update("/home/max/Work/thirdwave/zest/sparketl/spark-etl-test/datacreation/eligibility-sample.txt")

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
import random
from faker import Faker
import numpy as np
fake = Faker()


def random_delete_entry(input_file):
    spark = SparkSession\
        .builder\
        .appName("PySparkEligibiltyFile")\
        .getOrCreate()


    df = spark.read.json(input_file)



def random_file_update(input_file):
    updated_attributes = {"last_name": fake.last_name() ,"first_name": fake.first_name() ,"email": fake.email(), "city": fake.city(), "state": fake.state(), "zip_code": fake.zipcode(),
     "address_line_1": fake.street_address(),}
    updated_attributes_array = ["last_name","first_name","email","city","state","zip_code","address_line_1"]
    random_attribute = np.random.choice(updated_attributes_array)

    spark = SparkSession\
        .builder\
        .appName("PySparkEligibiltyFile")\
        .getOrCreate()

    df = spark.read.json(input_file)
    rows = df.collect()
    for row in rows:
        random_chance = random.randint(1, 100)
        if random_chance<=2:
            if(row[random_attribute]!= None):
                df = df.replace(row[random_attribute],updated_attributes[random_attribute],random_attribute)


    return(df)

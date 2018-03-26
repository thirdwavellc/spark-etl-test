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
import normalize



def eligibility_file_update(input_file):

    spark = SparkSession\
        .builder\
        .appName("PySparkEligibiltyFile")\
        .getOrCreate()


    df = spark.read.json(input_file)

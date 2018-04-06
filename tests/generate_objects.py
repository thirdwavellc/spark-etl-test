import csv
import sys, os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import models.schemas.radice as schemas
from models.data import *
from models.processors.radice import *
from models.entries.radice import *
from models.schemas.radice import *



def generate_objects_list(file):
    app_name = 'PySparkEligibiltyFile'
    spark_session = SparkSession.builder\
                        .appName(app_name)\
                        .getOrCreate()
    rows_list = LocalFileSparkDataSource(spark_session,schemas.eligibility_file,file)
    return(RadiceEtlProcessor(rows_list, eligibility_file))



def text_to_csv(file_location):
    txt_file = r"%s" % file_location
    csv_file = r"testing.csv"
    in_txt = csv.reader(open(txt_file, "rb"), delimiter = '|')
    out_csv = csv.writer(open(csv_file, 'wb'))

    out_csv.writerows(in_txt)

def panda_df(file):
    data = pd.read_csv(file, sep="|", header=None ,dtype=str)
    data.columns = ["source_id","client_name","field","run_date","employee_ssn","member_ssn","rel_to_subscriber","last_name",
    "first_name","date_of_birth","gender","benefit_type","coverage_level","group_number","ins_subscriber_id","member_id","plan_id","plan_name","coverage_start_date","coverage_end_date",
    "coverage_status","email","address_line_1","address_line_2","city","state","zip_code"]
    full_array = data.values.tolist()
    dic_array =[]
    for row in full_array:
        new_dict={}
        i=0
        for name in data.columns:
                new_dict[name]=row[i]
                i+=1
        dic_array.append(new_dict)
    return dic_array

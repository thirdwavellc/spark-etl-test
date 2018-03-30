from pyspark.sql.types import *
from pyspark.sql import SparkSession
import pandas
import paramiko
import json

def get_file_from_sftp(key_path,username):
    p_key = paramiko.RSAKey.from_private_key_file(key_path)
    con = paramiko.SSHClient()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect( hostname = "ec2-34-206-40-147.compute-1.amazonaws.com", username = username, pkey = p_key )
    sftp_con = con.open_sftp()
    return (sftp_con.open('/uploads/radice/eligibility-sample.txt'))

# TODO: move into library
def get_data_frame_list(schema,app_name):
    spark = SparkSession\
           .builder\
           .appName(app_name)\
           .getOrCreate()
    data = pandas.read_csv(get_file_from_sftp('/home/max/Downloads/radice-sftp.pem','radice'),sep='|',header=0)
    return((spark.createDataFrame(data,schema)).collect())

def file_partition_size(input_array,entries_per_file,path):
    i = 0
    file_number = 1
    while i < len(input_array):
        with open(path +'/data'+str(file_number)+'.json', 'w') as f:
            json.dump(input_array[i:i+entries_per_file], f)
        file_number +=1
        i += entries_per_file

from pyspark.sql.types import *
from pyspark.sql import SparkSession
import pandas
import paramiko
import json


class LocalFileSparkDataSource:

    def __init__(self, spark_session, schema, data_file,
                 header='false', delimiter='|'):
        self.spark_session = spark_session
        self.data = self.spark_session.read \
                        .format("CSV") \
                        .schema(schema) \
                        .option("header", header) \
                        .option("delimiter", delimiter) \
                        .option("treatEmptyValuesAsNulls", "true") \
                        .load(data_file) \

    def data_frames(self):
        return self.data.collect()


class SftpSparkDataSource:

    def __init__(self, spark_session, schema, sftp_connection, file_path,
                 header=0, sep='|'):
        self.spark_session = spark_session
        self.schema = schema
        self.data = pandas.read_csv(sftp_connection.open_file(file_path),
                                    sep=sep,
                                    header=header)

    def data_frames(self):
        return((self.spark_session.createDataFrame(self.data, self.schema))
               .collect())


class SftpConnection:

    def __init__(self, hostname, username, key_path):
        p_key = paramiko.RSAKey.from_private_key_file(key_path)
        con = paramiko.SSHClient()
        con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        con.connect(hostname=hostname, username=username, pkey=p_key)
        self.connection = con.open_sftp()

    def open_file(self, file_path):
        return self.connection.open(file_path)

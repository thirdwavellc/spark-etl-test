from pyspark.sql.types import *
from pyspark.sql import SparkSession
import pandas
import paramiko
import json


class LocalFileSparkDataSource:

    def __init__(self, spark_session, schema, data_file, header='false', delimiter='|'):
        """This object contains a spark session and a data_frame and reads in local files

        Args:
            spark_session: spark_session
            schema: Struct type
            data_file: str
            header: boolean (default="false")
            delimeter: str (default="|")

        """
        self.spark_session = spark_session
        self.data = self.spark_session.read \
                        .format("CSV") \
                        .schema(schema) \
                        .option("header", header) \
                        .option("delimiter", delimiter) \
                        .option("treatEmptyValuesAsNulls", "true") \
                        .load(data_file) \

    def to_row_list(self):
        """This function returns a list of row objects

        Args:
            None

        Yeild:
            list of spark row_objects
        """
        return self.data.collect()



class SftpSparkDataSource:

    def __init__(self, spark_session, schema, sftp_connection, file_path, header=None, sep='|'):
        """This object contains a spark session and a data_frame and reads in remote files

        Args:
            spark_session: spark_session
            schema: Struct type
            sftp_connection: paramiko sftp session object
            data_file: str
            header: boolean (default="false")
            delimeter: str (default="|")

        Attributes:
            data: DataFrame or TextParser
        """

        self.spark_session = spark_session
        self.schema = schema
        self.data = pandas.read_csv(sftp_connection.open_file(file_path),
                                    sep=sep,
                                    header=header,dtype=str)

    def to_row_list(self):
        """This function returns and list of row objects from the data frame object

        Args:
            None
        Yeild:
            list of spark row objects
        """

        return((self.spark_session.createDataFrame(self.data, self.schema))
               .collect())


class SftpConnection:

    def __init__(self, hostname, username, key_path):
        """This object creates a sftp connection utilizing paramiko

        Args:
            hostname: str
            username: str
            key_path: str

        """
        p_key = paramiko.RSAKey.from_private_key_file(key_path)
        con = paramiko.SSHClient()
        con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        con.connect(hostname=hostname, username=username, pkey=p_key)
        self.connection = con.open_sftp()

    def open_file(self, file_path):
        """This takes the connection and opens the file on the remote sftp server

        Args:
            file_path:str
        """
        return self.connection.open(file_path)

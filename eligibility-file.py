'''Converts sample Eligibilty file into JSON'''
from models.processors.radiceetlprocessor import RadiceEtlProcessor
from models.data_sources import SftpConnection, SftpSparkDataSource
import models.schemas.radice as schemas
from pyspark.sql.types import *
from pyspark.sql import SparkSession


def main():
    app_name = 'PySparkEligibiltyFile'
    spark_session = SparkSession.builder\
                        .appName(app_name)\
                        .getOrCreate()

    sftp_hostname = 'ec2-34-206-40-147.compute-1.amazonaws.com'
    sftp_user = 'radice'
    # TODO: find a location for this that's not user-specific
    key_path = '/home/max/Downloads/radice-sftp.pem'
    sftp_connection = SftpConnection(sftp_hostname, sftp_user, key_path)

    file_name = '/uploads/radice/eligibility-sample.txt'
    data_source = SftpSparkDataSource(spark_session, schemas.eligibility_file, sftp_connection, file_name)

    etl_process = RadiceEtlProcessor(data_source, schemas.eligibility_file)
    etl_process.process()
    etl_process.export()

if __name__ == "__main__":
    main()

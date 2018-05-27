'''Converts sample Eligibilty file into JSON using sftp data source'''
from models.processors.radice import RadiceEtlProcessor
from models.data.sources import SftpConnection, SftpSparkDataSource
import models.schemas.radice as schemas
from models.exporters.yaro import EligibilityExporter
from models.data.destinations import LocalFileDataWriter, RemoteFileDataWriter, LocalCsvWriter
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import os
from pathlib import Path


def main():
    app_name = 'PySparkEligibiltyFile'
    spark_session = SparkSession.builder\
                        .appName(app_name)\
                        .getOrCreate()

    sftp_hostname = 'ec2-34-206-40-147.compute-1.amazonaws.com'
    sftp_user = 'radice'
    key_path = os.path.join(Path.home(), 'radice-sftp.pem')
    sftp_connection = SftpConnection(sftp_hostname, sftp_user, key_path)

##TODO Commented this read in locally for now since we are not pulling the eligibility file from a real source right now and just showing
## how we are working with our dummy data.
    #file_name = '/uploads/radice/eligibility-sample.txt'
    #data_source = SftpSparkDataSource(spark_session, schemas.eligibility_file, sftp_connection, file_name)

    data_source = '/datacreation/eligibility-sample.txt'
    etl_process = RadiceEtlProcessor(data_source)
    etl_process.process()
    exporters = [
        EligibilityExporter(etl_process.valid_entries, LocalFileDataWriter('output/radice/yaro/passed/data.json')),
        EligibilityExporter(etl_process.invalid_entries, LocalFileDataWriter('output/radice/yaro/failed/data.json')),
        EligibilityExporter(etl_process.valid_entries, RemoteFileDataWriter(sftp_connection.connection,'uploads/radice/passed/data.json')),
        EligibilityExporter(etl_process.invalid_entries, RemoteFileDataWriter(sftp_connection.connection,'uploads/radice/failed/data.json')),

    ]
    etl_process.export(exporters)


if __name__ == "__main__":
    main()

'''Converts sample Eligibilty file into JSON'''
from models.processors.radice import RadiceEtlProcessor
from models.data.sources import SftpConnection, SftpSparkDataSource
import models.schemas.radice as schemas
from models.exporters.yaro import EligibilityExporter
from models.exporters.alegeus import CensusExporter
from models.data.destinations import LocalFileDataWriter
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

    etl_process = RadiceEtlProcessor(data_source)
    etl_process.process()
    exporters = [
        EligibilityExporter(etl_process.valid_entries, LocalFileDataWriter('output/radice/yaro/passed', 'data.json')),
        EligibilityExporter(etl_process.invalid_entries, LocalFileDataWriter('output/radice/yaro/failed', 'data.json')),
        # TODO: update census filenames once converted to EDI
        CensusExporter(etl_process.valid_entries, LocalFileDataWriter('output/radice/alegeus/passed', 'data.json')),
        CensusExporter(etl_process.invalid_entries, LocalFileDataWriter('output/radice/alegeus/failed', 'data.json'))
    ]
    etl_process.export()


if __name__ == "__main__":
    main()

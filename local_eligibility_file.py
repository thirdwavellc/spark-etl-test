'''Converts sample Eligibilty file into JSON using local data source'''

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.processors.radice import RadiceEtlProcessor
from models.data.sources import LocalFileSparkDataSource
import models.schemas.radice as schemas
from models.exporters.yaro import EligibilityExporter
from models.data.destinations import LocalFileDataWriter, LocalCsvWriter, RemoteFileDataWriter
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from models.data.sources import SftpConnection, SftpSparkDataSource
from pathlib import Path



def main():
    app_name = 'PySparkEligibiltyFile'
    spark_session = SparkSession.builder\
                        .appName(app_name)\
                        .getOrCreate()

    file_dir = os.path.dirname(__file__)
    data_file = os.path.join(file_dir, 'datacreation/eligibility-sample.txt')

    data_source = LocalFileSparkDataSource(spark_session, schemas.eligibility_file, data_file)

    etl_process = RadiceEtlProcessor(data_source)
    etl_process.process()

    exporters = [
        EligibilityExporter(etl_process.valid_entries, LocalFileDataWriter('output/radice/yaro/passed/data.json')),
        EligibilityExporter(etl_process.invalid_entries, LocalFileDataWriter('output/radice/yaro/failed/data.json')),
    ]
    etl_process.export(exporters)


if __name__ == "__main__":
    main()

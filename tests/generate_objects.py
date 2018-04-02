from pyspark.sql.types import *
from pyspark.sql import SparkSession
import models.schemas.radice as schemas
from models.data_sources import *
from models.processors.radiceetlprocessor import *
from models.entries.radice import *
from models.schemas.radice import *



def generate_objects_list(file):
    app_name = 'PySparkEligibiltyFile'
    spark_session = SparkSession.builder\
                        .appName(app_name)\
                        .getOrCreate()
    rows_list = LocalFileSparkDataSource(spark_session,schemas.eligibility_file,file)
    x = RadiceEtlProcessor(rows_list, eligibility_file)
    return (x)

import sys
from pyspark.sql.types import *
from ..validations import validations as valid
from ..normalizations import normalizations as norm
import etlprocessor as etlprocessor
from .. import helpfunctions as helper
from ..entries import radice as entries

class RadiceEtlProcessor(etlprocessor.EtlProcessor):
    def __init__(self, data_source, schema):
        self.schema = schema
        self.data_frame_list = data_source.data_frames()
        self.entries = self.create_entries()
        self.normalizations = [
            [norm.normalize_date_of_birth,"date_of_birth"],
            [norm.normalize_coverage_start_date,"coverage_start_date"],
            [norm.normalize_coverage_end_date,"coverage_end_date"],
            [norm.normalize_first_name,"first_name"],
            [norm.normalize_last_name,"last_name"],
            [norm.normalize_email,"email"],
            [norm.normalize_zip,"zip_code"],
            [norm.normalize_state,"state"]
        ]

        self.validations = [
            [valid.valid_dob,"date_of_birth"],
            [valid.valid_ssn,"member_ssn"],
            [valid.valid_first_name,"first_name"],
            [valid.valid_last_name,"last_name"],
            [valid.valid_email,"email"]
        ]

    # TODO: move to entry static method?
    def create_entries(self):
        return list(map(lambda data_frame: entries.EligibilityEntry(data_frame, self.schema), self.data_frame_list))

    def export(self):
        valid_entries_dic= list(map(lambda validator:self.return_fields(validator),self.valid_validators))
        invalid_entries_dic= list(map(lambda validator:self.return_fields(validator),self.invalid_validators))
        helper.file_partition_size(valid_entries_dic,1000000,'json/radice/passedentries')
        helper.file_partition_size(invalid_entries_dic,1000000,'json/radice/failedentries')

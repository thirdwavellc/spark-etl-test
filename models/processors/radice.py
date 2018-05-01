import sys
from ..validations import validations as valid
from ..normalizations import normalizations as norm
from .base import EtlProcessor
from ..entries.radice import EligibilityEntry


class RadiceEtlProcessor(EtlProcessor):

    def __init__(self, data_source):
        self.entries = list(map(lambda row: EligibilityEntry(row.asDict()), data_source.to_row_list()))

        self.normalizations = [
            [norm.normalize_date_of_birth, "date_of_birth"],
            [norm.normalize_coverage_start_date, "coverage_start_date"],
            [norm.normalize_coverage_end_date, "coverage_end_date"],
            [norm.normalize_first_name, "first_name"],
            [norm.normalize_last_name, "last_name"],
            [norm.normalize_email, "email"],
            #[norm.normalize_zip, "zip_code"],
            [norm.normalize_state, "state"]
        ]

        self.validations = [
            [valid.valid_dob, "date_of_birth"],
            #[valid.valid_ssn, "member_ssn"],
            [valid.valid_first_name, "first_name"],
            [valid.valid_last_name, "last_name"],
            [valid.valid_email, "email"]
        ]

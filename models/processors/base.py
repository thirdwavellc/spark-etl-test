import os
from datetime import date
import math
import operator
import csv
import sys
import paramiko
from ..validations import validations as valid
from ..normalizations import normalizations as norm


class EtlProcessor:

    def __init__(self, data_source):
        self.entries = []
        self.normalizations = []
        self.validations = []

    def process(self):
        self.normalize()
        self.validate()

    def normalize(self):
        list(map(lambda entry: norm.Normalizer(entry, self.normalizations).normalize(), self.entries))

    def filterdict(self,dic):
        ssns = ["member_ssn","employee_ssn"]
        for i in ssns:
            dic.pop(i)
        return(dic)

    def validate(self):
        self.validators = list(map(lambda entry: valid.Validator(entry,self.entries, self.validations).validate(), self.entries))
        self.valid_validators = list(filter(lambda validator: validator.has_errors() == False, self.validators))
        self.invalid_validators = list(filter(lambda validator: validator.has_errors() == True, self.validators))
        self.valid_entries = list(map(lambda validator: validator.entry.__dict__, self.valid_validators))
        self.valid_entries_nossn = list(map(lambda x: self.filterdict(x), self.valid_entries))
        self.invalid_entries = list(map(lambda validator: {"entry":validator.entry.__dict__, "errors":validator.errors}, self.invalid_validators))

    def export(self, exporters):
        for exporter in exporters:
            exporter.export()

import os
from datetime import date
import math
import operator
import csv
import sys
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import paramiko
import validations.validations as valid
import normalizations.normalizations as norm


class EtlProcessor:
    def process(self):
          self.normalize()
          self.validate()

    def normalize(self):
      list(map(lambda entry: norm.Normalizer(entry, self.normalizations).normalize(), self.entries))

    def validate(self):
      self.validators = list(map(lambda entry: valid.Validator(entry, self.validations).validate(), self.entries))
      self.valid_validators = filter(lambda validator: not validator.has_errors(), self.validators)
      self.invalid_validators = filter(lambda validator: validator.has_errors(), self.validators)


    #TODO this might be better to be a function in the entry class
    def return_fields(self,validator):
        entry_dic ={}
        for attr, value in validator.entry.__dict__.items():
            entry_dic[attr]=value
        return entry_dic

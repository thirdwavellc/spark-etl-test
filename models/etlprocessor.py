import os
from datetime import date
import math
import operator
from pyspark.sql.types import *
from pyspark.sql import SparkSession
import csv
import json
import sys
import paramiko
import validations.validations as valid
import entry as ent
import normalizations.normalizations as norm



class EtlProcessor:

    def process(self):
          self.normalize()
          self.validate()

    def create_entries(self):
      return list(map(lambda data_frame: ent.Entry(data_frame, self.eligibility_schema()), self.data_frame_list))

    def normalize(self):
      list(map(lambda entry: norm.Normalizer(entry, self.normalizations).normalize(), self.entries))


    def validate(self):
      self.validators = list(map(lambda entry: valid.Validator(entry, self.validations).validate(), self.entries))
      self.valid_validators = filter(lambda validator: not validator.has_errors(), self.validators)
      self.invalid_validators = filter(lambda validator: validator.has_errors(), self.validators)


    def return_fields(self,validator):
        entry_dic ={}
        for attr, value in validator.entry.__dict__.items():
            entry_dic[attr]=value
        return entry_dic


    def file_partition_size(self,input_array,entries_per_file,path):
        i = 0
        file_number = 1
        while i < len(input_array):
            with open(path +'/data'+str(file_number)+'.json', 'w') as f:
                json.dump(input_array[i:i+entries_per_file], f)
            file_number +=1
            i += entries_per_file

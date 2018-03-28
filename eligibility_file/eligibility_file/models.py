import collections


class Entry:
    def __init__(self, row_object, eligibility_schema):
            #created a variable for each field just for backup for now (was thinking of removing these and just using a single dictionary for easier customization for individual clients)
            self.source_id = str(row_object["source_id"])
            self.client_name = str(row_object["client_name"])
            self.field = str(row_object["field"])
            self.run_date = str(row_object["run_date"])
            self.employee_ssn = str(row_object["employee_ssn"])
            self.member_ssn = str(row_object["member_ssn"])
            self.rel_to_subscriber = str(row_object["rel_to_subscriber"])
            self.last_name = str(row_object["last_name"])
            self.first_name = str(row_object["first_name"])
            self.date_of_birth = str(row_object["date_of_birth"])
            self.gender =str(row_object["gender"])
            self.benefit_type = str(row_object["benefit_type"])
            self.coverage_level = str(row_object["coverage_level"])
            self.group_number= str(row_object["group_number"])
            self.ins_subscriber_id = str(row_object["ins_subscriber_id"])
            self.member_id = str(row_object["member_id"])
            self.plan_id  = str(row_object["plan_id"])
            self.plan_name = str(row_object["plan_name"])
            self.coverage_start_date = str(row_object["coverage_start_date"])
            self.coverage_end_date = str(row_object["coverage_end_date"])
            self.coverage_status = str(row_object["coverage_status"])
            self.email = str(row_object["email"])
            self.address_line_1 = str(row_object["address_line_1"])
            self.address_line_2 = str(row_object["address_line_2"])
            self.city=str(row_object["city"])
            self.state = str(row_object["state"])
            self.zip_code =str(row_object["zip_code"])





            #create a dictionary to store the fields of the eligibility_schema
            #this way seems like it will be easier than doing as I did above in creating a variable for each field
            #self.dictionary=collections.OrderedDict()
            #for field in eligibility_schema:
            #        self.dictionary[field.name] = str(row_object[field.name])


    #Returns an array of the dictionary if needed.
    def to_array(self,fields):
            new_array=[]
            for i in fields:
                    new_array.append(self.dictionary[i.name])
            return(new_array)

class Entry:
    def __init__(self, row_object, eligibility_schema):
            #created a variable for each field just for backup for now (was thinking of removing these and just using a single dictionary for easier customization for individual clients)
            self.source_id = row_object["source_id"]
            self.client_name = row_object["client_name"]
            self.field = row_object["field"]
            self.run_date = row_object["run_date"]
            self.employee_ssn = row_object["employee_ssn"]
            self.member_ssn = row_object["member_ssn"]
            self.rel_to_subscriber = row_object["rel_to_subscriber"]
            self.last_name = row_object["last_name"]
            self.first_name = row_object["first_name"]
            self.date_of_birth = row_object["date_of_birth"]
            self.gender =row_object["gender"]
            self.benefit_type = row_object["benefit_type"]
            self.coverage_level = row_object["coverage_level"]
            self.group_number= row_object["group_number"]
            self.ins_subscriber_id = row_object["ins_subscriber_id"]
            self.member_id = row_object["member_id"]
            self.plan_id  = row_object["plan_id"]
            self.plan_name = row_object["plan_name"]
            self.coverage_status = row_object["coverage_status"]
            self.email = row_object["email"]
            self.address_line_1 = row_object["address_line_1"]
            self.address_line_2 = row_object["address_line_2"]
            self.city=row_object["city"]
            self.state = row_object["state"]
            self.zip_code =row_object["zip_code"]


            #create a dictionary to store the fields of the eligibility_schema
            #this way seems like it will be easier than doing as I did above in creating a variable for each field
            self.dictionary=collections.OrderedDict()
            for field in eligibility_schema:
                    self.dictionary[field.name] = str(row_object[field.name])


    #Returns an array of the dictionary if needed.
    def to_array(self,fields):
            new_array=[]
            for i in fields:
                    new_array.append(self.dictionary[i.name])
            return(new_array)

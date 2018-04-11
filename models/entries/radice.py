class EligibilityEntry:

    def __init__(self, row_object):
            """Custom object created from a spark row object

            Note:

            Args:
                row_object (spark row_object): The paramter is a row object that is created by spark.
            """

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
            self.gender = str(row_object["gender"])
            self.benefit_type = str(row_object["benefit_type"])
            self.coverage_level = str(row_object["coverage_level"])
            self.group_number = str(row_object["group_number"])
            self.ins_subscriber_id = str(row_object["ins_subscriber_id"])
            self.member_id = str(row_object["member_id"])
            self.plan_id = str(row_object["plan_id"])
            self.plan_name = str(row_object["plan_name"])
            self.coverage_start_date = str(row_object["coverage_start_date"])
            self.coverage_end_date = str(row_object["coverage_end_date"])
            self.coverage_status = str(row_object["coverage_status"])
            self.email = str(row_object["email"])
            self.address_line_1 = str(row_object["address_line_1"])
            self.address_line_2 = str(row_object["address_line_2"])
            self.city = str(row_object["city"])
            self.state = str(row_object["state"])
            self.zip_code = str(row_object["zip_code"])


    def to_alegeus_census_dict(self):
        """Takes the current object and changes the fieldnames to match the alegeus census fields

        Args:
            None

        Yields:
            dict

        Examples:
            Entry = EligibilityEntry(row_dict)
            alegeus_dic = Entry.to_alegeus_census_dict
        """
        # TODO: evaluate required keys

        return {
            'record_header': 'FE',
            'tpa_id': '',
            'employer_id': 'ABC' + self.group_number,
            'employee_id': self.member_id,
            'prefix': '',
            'last_name': self.last_name,
            'first_name': self.first_name,
            'middle_initial': '',
            'phone': '',
            'address_line_1': self.address_line_1,
            'address_line_2': self.address_line_2,
            'city': self.city,
            'state': self.state,
            'zip': self.zip_code,
            'country': 'US',
            'email': self.email,
            'gender': self.gender,
            'martial_status': '',
            'birth_date': self.date_of_birth,
            'employee_ssn': self.member_ssn,
            'hdhp_eligible': '',
            'drivers_license_number': '',
            'mothers_maiden_name': '',
            'base_salary': '',
            'eligibility_date': self.coverage_start_date,
            'original_hire_date': '',
            'employment_type': '',
            'division': '',
            'employee_citizenship_status': '',
            'class_name': '',
            'record_track_number': '',
            'wealthcare_marketplace_employee_id': ''
        }

    def to_alegeus_demographics_dict(self):
        """Takes the current object and changes the fieldnames to match the alegeus demographics fields

        Args:
            None

        Yields:
            dict

        Examples:
            Entry = EligibilityEntry(row_dict)
            alegeus_dic = Entry.to_alegeus_demographics_dict
        """
        return{
            'record_id':'IB',
            'tpa_id':'',
            'employer_id': 'ABC' + self.group_number,
            'employee_id':self.member_id,
            'prefix':'',
            'last_name':self.last_name,
            'first_name':self.first_name,
            'middle_initial':'',
            'phone':'',
            'mobile_number':'',
            'address_line_1':self.address_line_1,
            'address_line_2':self.address_line_2,
            'city':self.city,
            'state':self.state,
            'zip':self.zip_code,
            'country':'US',
            'reimbursment_method':'',
            'email':self.email,
            'user_defined_field':'',
            'employee_status':'',
            'gender':self.gender,
            'martial_status':'',
            'shipping_address_line_1':'',
            'shipping_address_line_2':'',
            'shipping_address_city':'',
            'shipping_address_state':'',
            'shipping_address_zip':'',
            'shipping_address_country':'',
            'birth_date':self.date_of_birth,
            'bank_routing_number':'',
            'bank_account_number':'',
            'bank_account_type_code':'',
            'bank_name':'',
            'remarks':'',
            'employee_ssn':self.employee_ssn,
            'health_plan_id':'',
            'dental_id':'',
            'vision_id':'',
            'pbm_id':'',
            'health_coverage_default':'',
            'medical_coverage':'',
            'pharmacy_coverage':'',
            'dental_coverage':'',
            'hospital_coverage':'',
            'vision_coverage':'',
            'hearing_coverage':'',
            'card_design':'',
            'high_deductible_health_plan_eligible':'',
            'employee_drivers_license_number':'',
            'employee_mother_maiden_name':'',
            'communication_options':'',
            'medicare_beneficiary':'',
            'medicare_id':'',
            'record_tracking_number':'',
            'employee_processing_notes':'',
            'mobile_communication_options':'',
            'person_code':'',
            'end_state_renal_disease':'',
            'wealthcare_marketplace_employee_id':'',
        }

    def from_data_frame_list(row_list):
        """Returns a list of EligibilityEntry objects

        Args:
            row_list: list of spark row objects

        Yields:
            A list of spark row objects

        """
        return list(map(lambda data_frame: EligibilityEntry(data_frame),
                        row_list))

# TODO: evaluate argparse.Namespace for simple value objects
class CensusEntry:

    # TODO: extract value mapping to client-specific class
    def __init__(self, eligibility_entry):
        self.record_header = 'FE'
        self.tpa_id = ''
        self.employer_id = 'ABC' + eligibility_entry.group_number
        self.employee_id = eligibility_entry.member_id
        self.prefix = ''
        self.last_name = eligibility_entry.last_name
        self.first_name = eligibility_entry.first_name
        self.middle_initial = ''
        self.phone = ''
        self.address_line_1 = eligibility_entry.address_line_1
        self.address_line_2 = eligibility_entry.address_line_2
        self.city = eligibility_entry.city
        self.state = eligibility_entry.state
        self.zip = eligibility_entry.zip_code
        self.country = 'US'
        self.email = eligibility_entry.email
        self.gender = eligibility_entry.gender
        self.martial_status = ''
        self.birth_date = eligibility_entry.date_of_birth
        self.employee_ssn = eligibility_entry.member_ssn
        self.hdhp_eligible = ''
        self.drivers_license_number = ''
        self.mothers_maiden_name = ''
        self.base_salary = ''
        self.eligibility_date = eligibility_entry.coverage_start_date
        self.original_hire_date = ''
        self.employment_type = ''
        self.division = ''
        self.employee_citizenship_status = ''
        self.class_name = ''
        self.record_track_number = ''
        self.wealthcare_marketplace_employee_id = ''

    @staticmethod
    def from_eligibility_entries(eligibility_entries):
        return list(map(lambda entry: CensusEntry(entry), eligibility_entries))

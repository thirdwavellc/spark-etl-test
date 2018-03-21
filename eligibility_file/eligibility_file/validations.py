class Result:
    def __init__(self, passed, error=""):
        self.passed = passed
        self.failed = not passed
        self.error = error

class Validator:
    def __init__(self, entry, validations=[]):
        self.entry = entry
        self.validations = validations
        self.errors = []

    def validate(self):
        self.__clear_errors()
        validation_results = list(map(lambda validation: validation(self.entry), self.validations))
        failed_validations = list(filter(lambda validation: validation.failed), validation_results)
        self.errors = list(map(lambda validation: validation.error))
        return len(self.errors) == 0

    def __clear_errors(self):
        self.errors = []

def has_valid_dob(entry):
    # TODO: implement me for real
    passed = True
    return Result(passed)

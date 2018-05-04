import datetime
import random
from functools import reduce
from faker import Faker
import numpy as np




now = datetime.datetime.now()
fake = Faker()

def percent_chance(percent):
    """Returns true or false if the randome number choosen is less that in input. Ex if you input 10 there is a 10 percent chance that the function returns true.

    Args:
        percent:int

    Returns:
        Boolean

    """
    return random.randint(1, 100) <= percent


#Part that adds arbitrary space to any string
def add_random_space(percent,string_var):
    """Takes a percent chance and a string variable to insert a random space at a random location within the string. Ex add_random_space(10,"hello") would insert a random space somewhere
    within the string only 10 percent of the time and 90 percent of the time it returns the original input string parameter.

    Args:
        percent:int
        string_var:str

    Returns:
        str

    """
    if(percent_chance(percent)):
        string_length=len(string_var)
        random_location = random.randint(1,string_length)
        string_var = string_var[:random_location] + " " + string_var[random_location:]
    return(string_var)

def add_alpha_char(percent,string):
    """Adds a random alpaha character to a string. Used for adding letters to fields that should not contain letters such as zip code, for testing validation later on.

    Args:
        percent:int
        string:str

    Returns:
        str

    """
    if(percent_chance(percent)):
        characters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X',
        'Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w',
        'x','y','z']
        string_len = len(string)
        random_character = np.random.choice(characters)
        random_location = random.randint(1,string_length)
        string = string[:random_location] + random_character + string[random_location:]

    return(string)





class EligibilityFile:

    def __init__(self, client):
        """This object takes a client object. A client has many subscribers. Subscribers are people that work directly for a client and are also members. Members don't nececarily
        work for the client, but have a health plan that maybe through a subscriber.

        Args:
            client: Client object

        """
        self.client = client

    def write(self, filename):
        """This function writes all the members of a client to a psv text file. Each field is separated by a pipe instead of the usual comma.

        Args:
            filename: str


        Returns:
            None (writes file to folder)

        """
        eligibility_file = open(filename, 'w')

        for group in self.client.groups:
            for subscriber in group.subscribers:
                for member in subscriber.members:
                    eligibility_file.write(member.to_psv())

        eligibility_file.close()

class Client:
    def __init__(self, num_groups=250, num_subscribers=15000, min_group_size=5, max_group_size=500, uses_ssn=False, name='Radice', source_id='RADICE'):
        """The client object has many members. The members were divided into groups because we thought that the client might have grouped there members into groups for organizationself,
        however we me find this may not be the case.

        Args:
            num_groups: int (default=250)
            num_subscribers: int (default=15000)
            min_group_size: int (default=5)
            max_group_size: int (default=500)
            uses_ssn: boolean (default=False)



        # TODO: maybe change num_subscribers to num_members since it is actually the number of members instead of number of subscribers
        """
        self.num_groups = num_groups
        self.num_subscribers = num_subscribers
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size
        self.uses_ssn = uses_ssn
        self.client_name = name
        self.source_id = source_id
        self.groups = []
        self.generate_groups()

    def total_members(self):
        """Gets the total members that the clients has by adding up the total members in each group.

        Args:
            None


        Returns:
            int

        """
        if len(self.groups) == 0:
            return 0
        return reduce(lambda x, y: x + y, map(lambda group: group.total_members(), self.groups))

    def generate_groups(self):
        """This function creates a list of group objects.

        Args:
            None

        Returns:
            Array of group obejcts

        """
        group_sizes = [random.randint(self.min_group_size, self.max_group_size)]
        while reduce(lambda x, y: x + y, group_sizes) < self.num_subscribers:
            subscribers_remaining = self.num_subscribers - reduce(lambda x, y: x + y, group_sizes)
            if subscribers_remaining <= self.min_group_size or subscribers_remaining <= self.max_group_size:
                group_sizes.append(subscribers_remaining)
            else:
                group_sizes.append(random.randint(self.min_group_size, self.max_group_size))

        for group_size in group_sizes:
            print("Creating group with size {0}".format(group_size))
            self.groups.append(Group(self, group_size))

class Group:

    PLANS = [['HumanaHMO', '85945180'],
             ['HumanaHDHP 08','58330876'],
             ['Humana ChoicePOS 080','99610784']]

    def __init__(self, client, num_subscribers):
        """Gets the total members that the clients has by adding up the total members in each group.

        Attrbutes:
            Plans: 2d-array that contains two strings
        Args:
            client: Client object
            num_subscribers: int


        """
        self.client = client
        self.group_number = fake.ean(length=8)
        self.subscribers = []
        self.generate_subscribers(num_subscribers)

    def total_members(self):
        """This function list all the members in a single groupd

        Args:
            None

        Returns:
            int

        """
        if len(self.subscribers) == 0:
            return 0
        return reduce(lambda x, y: x + y, map(lambda subscriber: subscriber.total_members(), self.subscribers))

    def generate_subscribers(self, num_subscribers):
        """The function takes the num of subscribers in the group and keeps appending the subscriber to the subscibers list until it has gone though all the the subscibers

        Note:
            the if statement is used to added duplicate subscibers 1 perecent of the time.

        Args:
            num_subscribers: int

        Returns:
            Array of subscibers

        """
        email_storage = []

        while self.total_members() < num_subscribers:
            self.subscribers.append(Subscriber(self))
            ## TODO: Need to fix how records are duplicated this way duplicates subscriber info but the Member info changes and is not the same.
            #random_number = random.randint(0, 99)
            #if random_number <=1:
            #    self.subscribers.append(Subscriber(self))
            #    self.subscribers.append(Subscriber(self))
            #else:


# TODO: include new enrollment year records

class Subscriber:
    COVERAGE_LEVELS = ['EO', 'ES', 'EC', 'EF']

    def __init__(self, group):
        """This is a subsciber object. A subsciber is on that is an employee of a client. A subsciber is a special type of member.

        Attrbutes:
            COVERAGE_LEVELS: array of string values
        Args:
            group: Group object


        """
        self.group = group
        self.coverage_level = np.random.choice(self.COVERAGE_LEVELS,1,p=[0.28, 0.17,0.17,0.38])[0]
        self.benefit_type = 'Medical'
        self.ins_subscriber_id = '' if self.group.client.uses_ssn else fake.bban()
        self.plan = random.choice(self.group.PLANS)
        self.plan_id = self.plan[1]
        self.plan_name = self.plan[0]
        self.coverage_start_date = fake.date_between(start_date='-9m', end_date='+3m').replace(day=1)
        self.coverage_end_date = self.coverage_start_date.replace(year=self.coverage_start_date.year + 1, month=self.coverage_start_date.month - 1, day=1)
        self.coverage_status = self.coverage_start_date <= now.date() <= self.coverage_end_date
        self.employee = Member(self, 0, '001')
        self.dependants = self.generate_dependants()
        self.members = [self.employee] + self.dependants

    def total_members(self):
        """Returns the total number of members. This is the subsciber plus any dependants

        Args:
            None

        Return:
            int
        """
        return len(self.members)

    def generate_dependants(self):
        """Generates dependants for a subsciber. This uses a probability distribution function, for ex the chance of having a 5 person family is smaller than having
        a two person family. Actual accurate numbers used for the function.

        Args:
            None

        Return:
            An array of members
        """
        eflist  = np.random.choice([[Member(self, 1, '002'), Member(self, 2, '003')],[Member(self, 1, '002'), Member(self, 2, '003'),Member(self, 2, '004')],
        [Member(self, 1, '002'), Member(self, 2, '003'),Member(self, 2, '004'),Member(self, 2, '005')],[Member(self, 1, '002'), Member(self, 2, '003'),Member(self, 2, '004'),Member(self, 2, '005'),
        Member(self, 2, '006')]],1,p=[.40,.34,.16,.10])[0]

        return {
            'EO': [],
            'ES': [Member(self, 1, '002')],
            'EC': [Member(self, 2, '002')],
            'EF': eflist

        }[self.coverage_level]



class Member:

    def __init__(self, subscriber, rel_to_subscriber, subscriber_num):
        """The is the base Member object. Even subscibers are members.

        Args:
            subsciber: Subscriber object
            rel_to_subscriber: str
            subsciber_num: str


        """
        self.subscriber = subscriber
        self.rel_to_subscriber = rel_to_subscriber

        if self.rel_to_subscriber==0:
            self.original_last_name = fake.last_name()
            self.last_name = add_random_space(5,self.original_last_name)
        else:
            self.original_last_name = self.subscriber.employee.last_name
            self.last_name = add_random_space(1,self.original_last_name)

        self.first_name = fake.first_name()
        self.first_name = add_random_space(100,self.first_name)
        self.date_of_birth = fake.date_between(start_date='-58y', end_date='-18y')
        if self.rel_to_subscriber==2:
            self.date_of_birth = fake.date_between(start_date='-38y', end_date='-18y')
        self.gender = 'M' if percent_chance(50) else 'F'
        self.ssn = fake.ssn() if self.subscriber.group.client.uses_ssn else ''
        self.member_id = '' if self.subscriber.group.client.uses_ssn else self.subscriber.ins_subscriber_id + ' ' + subscriber_num

        mail_extension = np.random.choice(["@gmail.com","@yahoo.com","@hotmail.com","@aol.com"])
        email_storage = []
        self.email = add_random_space(2, self.first_name+ self.original_last_name + mail_extension)
        email_storage.append(self.email)
        if self.email in email_storage:
            self.email = fake.email()
        email_storage.append(self.email)
        self.address_line_1 = fake.street_address() if self.is_employee() else ''
        self.address_line_2 = fake.secondary_address() if self.is_employee() and percent_chance(30) else ''
        self.city = fake.city() if self.is_employee() else ''
        self.state = fake.state_abbr() if self.is_employee() else ''
        self.zipcode = fake.zipcode() if self.is_employee() else ''

    def is_employee(self):
        """Checks to see if the member is a subsciber or not. (In other words are they an employee?)

        Args:
            None

        Return:
            Boolean
        """
        return self.rel_to_subscriber == 0

    def to_psv(self):
        """Returns a string of all the member attributes. The fields are separated by |.

        Args:
            None

        Return:
            str
        """
        return '|'.join([
            str(self.subscriber.group.client.source_id),
            str(self.subscriber.group.client.client_name),
            str('MEM'),
            str(now.strftime('%Y%m%d')),
            str(self.subscriber.employee.ssn),
            str(self.ssn),
            str(self.rel_to_subscriber),
            str(self.last_name),
            str(self.first_name),
            str(self.date_of_birth),
            str(self.gender),
            str(self.subscriber.benefit_type),
            str(self.subscriber.coverage_level),
            str(self.subscriber.group.group_number),
            str(self.subscriber.ins_subscriber_id),
            str(self.member_id),
            str(self.subscriber.plan_id),
            str(self.subscriber.plan_name),
            str(self.subscriber.coverage_start_date),
            str(self.subscriber.coverage_end_date),
            str(self.subscriber.coverage_status),
            str(self.email),
            str(self.address_line_1),
            str(self.address_line_2),
            str(self.city),
            str(self.state),
            str(self.zipcode)
        ]) + '\n'


sample_client = Client(num_groups=25, num_subscribers=15000, uses_ssn=False)
sample_eligibility_file = EligibilityFile(sample_client)

sample_eligibility_file.write('eligibility-sample.txt')

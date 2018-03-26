import datetime
import random
from functools import reduce
from faker import Faker
import numpy as np

now = datetime.datetime.now()
fake = Faker()

def percent_chance(percent):
    return random.randint(1, 100) <= percent


#Part that adds arbitrary space to any string
def add_random_space(percent,string_var):
    if(percent_chance(percent)):
        string_length=len(string_var)
        random_location = random.randint(1,string_length)
        string_var = string_var[:random_location] + " " + string_var[random_location:]
    return(string_var)

class EligibilityFile:
    def __init__(self, client):
        self.client = client

    def write(self, filename):
        eligibility_file = open(filename, 'w')

        for group in self.client.groups:
            for subscriber in group.subscribers:
                for member in subscriber.members:
                    eligibility_file.write(member.to_psv())

        eligibility_file.close()

class Client:
    def __init__(self, num_groups=250, num_subscribers=15000, min_group_size=5, max_group_size=500, uses_ssn=False):
        self.num_groups = num_groups
        self.num_subscribers = num_subscribers
        self.min_group_size = min_group_size
        self.max_group_size = max_group_size
        self.uses_ssn = uses_ssn
        self.client_name = fake.company()
        self.source_id = self.client_name.split(' ')[0].replace(',', '')
        self.groups = []
        self.__generate_groups()

    def total_members(self):
        if len(self.groups) == 0:
            return 0
        return reduce(lambda x, y: x + y, map(lambda group: group.total_members(), self.groups))

    def __generate_groups(self):
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
    PLANS = [['Example PPO', fake.ean(length=8)],
             ['Example HSA', fake.ean(length=8)],
             ['Example HMO', fake.ean(length=8)]]

    def __init__(self, client, num_subscribers):
        self.client = client
        self.group_number = fake.ean(length=8) if percent_chance(50) else ''
        self.subscribers = []
        self.__generate_subscribers(num_subscribers)

    def total_members(self):
        if len(self.subscribers) == 0:
            return 0
        return reduce(lambda x, y: x + y, map(lambda subscriber: subscriber.total_members(), self.subscribers))

    def __generate_subscribers(self, num_subscribers):
        while self.total_members() < num_subscribers:
            random_number = random.randint(0, 99)
            if random_number <=1:
                self.subscribers.append(Subscriber(self))
                self.subscribers.append(Subscriber(self))
            else:
                self.subscribers.append(Subscriber(self))

# TODO: include new enrollment year records

class Subscriber:
    COVERAGE_LEVELS = ['EO', 'ES', 'EC', 'EF']

    def __init__(self, group):
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
        return len(self.members)

    def generate_dependants(self):

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
        self.subscriber = subscriber
        self.rel_to_subscriber = rel_to_subscriber
        if self.rel_to_subscriber==0:
            self.last_name = fake.last_name()
            self.last_name = add_random_space(1,self.last_name)
        else:
            self.last_name = self.subscriber.employee.last_name
            self.last_name = add_random_space(1,self.last_name)

        self.first_name = fake.first_name()
        self.first_name = add_random_space(1,self.first_name)
        self.date_of_birth = fake.date_between(start_date='-58y', end_date='-18y')
        self.rel_to_subscriber==2:
            self.date_of_birth = fake.date_between(start_date='-38y', end_date='-18y')
        self.gender = 'M' if percent_chance(50) else 'F'
        self.ssn = fake.ssn() if self.subscriber.group.client.uses_ssn else ''
        self.member_id = '' if self.subscriber.group.client.uses_ssn else self.subscriber.ins_subscriber_id + ' ' + subscriber_num

        mail_extension = np.random.choice(["@gmail.com","@yahoo.com","@hotmail.com","@aol.com"])
        self.email = self.first_name + self.last_name + mail_extension
        self.address_line_1 = fake.street_address() if self.is_employee() else ''
        self.address_line_2 = fake.secondary_address() if self.is_employee() and percent_chance(30) else ''
        self.city = fake.city() if self.is_employee() else ''
        self.state = fake.state_abbr() if self.is_employee() else ''
        self.zipcode = fake.zipcode() if self.is_employee() else ''

    def is_employee(self):
        return self.rel_to_subscriber == 0

    def to_psv(self):
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


sample_client = Client(num_groups=25, num_subscribers=1500, uses_ssn=False)
sample_eligibility_file = EligibilityFile(sample_client)

sample_eligibility_file.write('eligibility-sample.txt')

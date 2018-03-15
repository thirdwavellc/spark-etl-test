require 'faker'
require 'active_support/all'

FIELDS = [:source_id, :client_name, :field, :run_date, :employee_ssn,
          :member_ssn, :rel_to_subscriber, :last_name, :first_name,
          :date_of_birth, :gender, :benefit_type, :coverage_level,
          :group_number, :ins_subscriber_id, :member_id, :plan_id, :plan_name,
          :coverage_start_date, :coverage_end_date, :coverage_status, :email,
          :address_line_1, :address_line_2, :city, :state, :zip_code]

class Member
  attr_reader(*FIELDS)

  def initialize
    @source_id = Faker::App.name
    @client_name = Faker::Company.name
    @field = 'MEM'
    @run_date = Date.today.strftime("%Y%m%d")
    @employee_ssn = percent_chance?(20) ? Faker::IDNumber.valid : ''
    @member_ssn = @employee_ssn
    @rel_to_subscriber = 0
    @last_name = Faker::Name.last_name
    @first_name = Faker::Name.first_name
    @date_of_birth = Faker::Date.between(58.years.ago, 18.years.ago)
    @gender = ['M', 'F'].sample
    @benefit_type = 'Medical'
    @coverage_level = 'EO'
    @group_number = percent_chance?(50) ? Faker::Number.number(7) : ''
    @ins_subscriber_id = @employee_ssn.empty? ? Faker::Bank.swift_bic : ''
    @member_id = @employee_ssn.empty? ? "#{@ins_subscriber_id} 001" : ''
    @plan_id = percent_chance?(70) ? Faker::Number.number(5) : ''
    @plan_name = Faker::App.name
    @coverage_start_date = (Faker::Date.between(9.months.ago, 3.months.from_now).beginning_of_month).strftime("%Y%m%d")
    @coverage_end_date = (@coverage_start_date.to_date + 1.year - 1.day).strftime("%Y%m%d")
    @coverage_status = Date.today.between?(@coverage_start_date.to_date, @coverage_end_date.to_date) ? 'A' : 'I'
    @email = percent_chance?(30) ? Faker::Internet.email(@first_name) : ''
    @address_line_1 = Faker::Address.street_address
    @address_line_2 = percent_chance?(30) ? Faker::Address.secondary_address : ''
    @city = Faker::Address.city
    @state = Faker::Address.state_abbr
    @zip_code = Faker::Address.zip_code
  end

  def to_psv
    FIELDS.map { |attr| send(attr) }.join('|') + "\n"
  end

  private

  def percent_chance?(num)
    Faker::Number.between(1, 100) <= num
  end
end

members = (1..15000).map { Member.new }

File.open('eligibility-sample.txt', 'w') { |file| members.each { |member| file.write(member.to_psv) } }

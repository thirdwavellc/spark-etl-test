###Running
These files are used to create dummy data for the etl process to use.

The eligibility file is the main file that generates the baseline data. It can be run simply by running
    
    python eligibility_file_generator.py

in the command line and the output file will be a text file name "eligibility-sample.txt".

There is a second file in this folder named eligibility update. This file is used to add percentage amout of random field changes to the eligibility text file. It then create another file named "transformed-text-data.txt". This is the file that is then sent to the spark etl process. To run this file simply do

    python eligibilityupdate.py

the file will be generated in the same folder.

###Install Notes (mac):

    sudo easy_install pip
    
    pip3 install virtualenv
    pip3 install virtualenvwrapper
    pip3 install faker
    pip3 install numpy
    pip3 install pyspark
    pip3 install pandas
    pip3 install validate_email
    pip3 install zipcodes
    pip3 install paramiko

https://stackoverflow.com/questions/30518362/how-do-i-set-the-drivers-python-version-in-spark

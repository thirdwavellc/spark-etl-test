## Running

These files are used to create dummy data for the etl process to use.

The eligibility file is the main file that generates the baseline data. It can be run simply by running
    
    python eligibility_file_generator.py

in the command line and the output file will be a text file name "eligibility-sample.txt".

There is a second file in this folder named eligibility update. This file is used to add percentage amout of random field changes to the eligibility text file. It then create another file named "transformed-text-data.txt". This is the file that is then sent to the spark etl process. To run this file simply do

    python eligibilityupdate.py

the file will be generated in the same folder.

## Install Notes (mac):

    sudo easy_install pip
    pip install -r requirements.txt
    
## Configuration

You will need to ensure that python3 is used as the runner for spark. Inside the downloaded Spark server,
add the following settings at the end of the conf/spark-env.sh file ( create this file from the template if necessary) 

    PYSPARK_PYTHON=python3 
    PYSPARK_DRIVER_PYTHON=python3

More information here:
https://stackoverflow.com/questions/30518362/how-do-i-set-the-drivers-python-version-in-spark

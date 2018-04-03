#!/bin/bash

echo "Running python eligibility file..."
./spark-2.2.1-bin-hadoop2.7/bin/spark-submit --master spark://127.0.0.1:7077 ./remote_eligibility_file.py

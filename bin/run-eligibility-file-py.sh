#!/bin/bash

echo "Deleting previous eligibility runs..."
rm -rf ./eligibility-sample-20*
echo "Running python eligibility file..."
./spark-2.2.1-bin-hadoop2.7/bin/spark-submit --master spark://127.0.0.1:7077 ./eligibility-file.py


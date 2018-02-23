#!/bin/bash

echo "Starting master..."
./spark-2.2.1-bin-hadoop2.7/sbin/start-master.sh --host 127.0.0.1
echo "Starting worker..."
./spark-2.2.1-bin-hadoop2.7/sbin/start-slave.sh --host 127.0.0.1 spark://127.0.0.1:7077

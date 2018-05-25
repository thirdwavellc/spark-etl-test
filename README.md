# Spark ETL Test

This repo includes the [Spark][Spark] ETL jobs for Yaro.

[Spark][Spark] has been selected due to its flexibilty of running standalone as
an open source package, as well as its integration into the [AWS Glue][AWS
Glue] service. Out of the box, [Spark][Spark] has bindings for Java, Scala,
Python, and R.

## Setup

### Download Spark

To keep the repo size down, we do not include the [Spark][Spark] installation. Work so
far has been tested with [Spark][Spark] release 2.2.1, with the pre-build Hadoop 2.7 and
later package. You will need to download and unzip this file into the root of
this repo:

  http://mirrors.sorengard.com/apache/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz

In case this mirror is unavailable, the download can be selected here:

  https://spark.apache.org/downloads.html

### Start Spark master and worker processes

Once you have [Spark][Spark] downloaded/unzipped, you can use the following script to start
the master and worker processes:

```bash
$ bin/start.sh
```

To stop the processes, you can use the following script:

```bash
$ bin/stop.sh
```

The [Spark][Spark] Master UI is available at
[http://localhost:8080/](http://localhost:8080/).

## Python Eligibility File ETL Process

To test the python Eligibility file ETL process, we currently have two scripts:

- bin/run-local-eligibility-file-py.sh
- bin/run-remote-eligibility-file-py.sh

Both scripts process the same dataset, however one is using a local source
file, while the other is using a remote source file over SFTP. In most cases,
you can just use the local script, as it won't require you to have the
necessary credentials for the SFTP server. In order to run the remote script,
you must have the `radice-sftp.pem` key file in your home directory. This key
file is not included in the repo, and will be shared as needed.

[Spark]: https://spark.apache.org/
[AWS Glue]: https://aws.amazon.com/glue/
[Mobius]: https://github.com/Microsoft/Mobius

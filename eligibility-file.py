'''Converts sample Eligibilty file into JSON'''
import models.processors.radiceetlprocessor as client


def main():
    etl_process = client.RadiceEtlProcessor()
    etl_process.process()
    etl_process.export()


if __name__ == "__main__":
    main()

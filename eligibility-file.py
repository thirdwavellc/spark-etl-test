'''Converts sample Eligibilty file into JSON'''
import models.radicaletalprocessor as client









def main():
    etl_process = client.RadiceEtlProcessor()
    etl_process.process()
    etl_process.export()





if __name__ == "__main__":
    main()

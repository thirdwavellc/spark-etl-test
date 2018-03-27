import os, sys
import time



def main():
    x = t.Normalized("T      EST","H A N S E N")
    x.normalize_first_name()
    x.normalize_last_name()
    print(x.first_name)
    print(x.last_name)





def valid_date(date):


    try:
        valid_date = time.strptime(date, '%m-%d-%Y')
    except ValueError:
        try:
            valid_date = time.strptime(date, '%m/%d/%Y')

        except ValueError:
            try:
                valid_date = time.strptime(date, '%m%d%Y')

            except ValueError:
                return(False)
    return(True)


#def no_spaces():



#def title_case():




#def valid_ssn():



#def valid_email():


#def valid_zip():











if __name__ == "__main__":
    main()

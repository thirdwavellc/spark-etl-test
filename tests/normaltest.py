import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py

import test2 as t



def main():
    x = t.Normalized("T      EST","H A N S E N")
    x.normalize_first_name()
    x.normalize_last_name()
    print(x.first_name)
    print(x.last_name)




if __name__ == "__main__":
    main()

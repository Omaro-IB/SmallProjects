"""
Summary: CUPED implementation with CSVs
Requirements: a CSV file with one column for the pre-treatment, another for the post-treatment, and one binary column
with 1s and 0s (1 for received treatment and 0 for control)
Usage: python CUPED-P.py [CSV Directory] [Pre-Treatment Column] [Post-Treatment Column] [Binary Column] (options)
    Options: -s or --show: show the distribution graph in your browser
"""
import traceback

import CUPED
import sys
import pandas.errors
from patsy import PatsyError

arguments = sys.argv
show = False

# Check for optional arguments
if len(arguments) > 4:
    for arg in arguments[5:]:
        if not (arg.lower() == "-s" or arg.lower() == "--show"):
            print("Invalid Argument {}".format(arg))
            exit(1)
        else:
            show = True


# Check for help
if len(arguments) == 1 or arguments[1].lower() == "help" or arguments[1] == "?" or arguments[1].lower() == "-h":
    print("""Usage: python CUPED-P.py [CSV Directory] [Pre-Treatment Column] [Post-Treatment Column] [Binary Column] (options)
    Options: -s or --show: show the distribution graph in your browser""")
    exit(0)


# check for bad number of arguments
if len(arguments) != 5:
    if len(arguments) != 6 or not show:
        print("Bad number of arguments")
        print("""Usage: python CUPED-P.py [CSV Directory] [Pre-Treatment Column] [Post-Treatment Column] [Binary Column] (options)
        Options: -s or --show: show the distribution graph in your browser""")
        exit(1)
            

# Run the program
try:
    ATE, ATE_CUPED, Variance, Variance_CUPED, percChangeReg, percChangeCUPED = CUPED.CUPED_csv(arguments[1], arguments[2], arguments[3], arguments[4], show=show)
except PermissionError:
    print("Permission Error for Directory {}\nPlease check your inputted directory or perhaps the _CUPED.csv file is open".format(arguments[1]))
    exit(1)
except pandas.errors.EmptyDataError:
    print("Data error: please make sure your CSV file is formatted correctly")
    exit(1)
except FileNotFoundError:
    print("File {} not found".format(arguments[1]))
    exit(1)
except KeyError as ex:
    print("Bad binary column name")
    exit(1)
except PatsyError:
    print("Bad pre/post column name, please check your input and your CSV file")
    exit(1)
except Exception as ex:
    print("Unexpected Error {}".format(ex))
    exit(1)

    
print("Average Treatment Effect Before CUPED: {}".format(ATE))
print("Average Treatment Effect After CUPED: {}".format(ATE_CUPED))

print("Variance Before CUPED: {}".format(Variance))
print("Variance After CUPED: {}".format(Variance_CUPED))

print("Percentage Change (Control to Treatment) Before CUPED: {}%".format(round(percChangeReg*100, 2)))
print("Percentage Change (Control to Treatment) After CUPED: {}%".format(round(percChangeCUPED*100, 2)))

exit(0)

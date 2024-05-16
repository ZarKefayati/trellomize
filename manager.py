import argparse


parser = argparse.ArgumentParser() 

parser.add_argument('newPerson')           # positional argument
parser.add_argument('--username')      # option that takes a value
parser.add_argument('--password')  # on/off flag

args = parser.parse_args()

print(args)

# args = parser.parse_args()
# print(args.filename, args.count, args.verbose)
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-N', type=int,
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args)
print(type(args.N))
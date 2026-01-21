import argparse
from lpm import download
from lpm import repositories

parser = argparse.ArgumentParser(description='Package manager for Lumin Linux')

parser.add_argument('-I', "--install", nargs='+', help='install package')
parser.add_argument('-R', "--repository", default="stable", help='select repository for download package')
parser.add_argument("-o", "--output", default="/tmp/lpm", help = 'set install package output location')

args = parser.parse_args()

download.download_package(package=args.install[0], repository=args.repository, output=args.output)
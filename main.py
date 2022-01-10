import pandas as pd
from utils import process, rolling_sum_race, total_count_race
import argparse

rootdir = 'messages/inbox'

parser = argparse.ArgumentParser()
parser.add_argument("--days", required=True)

args = parser.parse_args()


if __name__ == '__main__':
    df = process()
    if args.days == 'all':
        total_count_race(df)
    else:
        rolling_sum_race(df, int(args.days))
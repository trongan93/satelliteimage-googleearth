import sys
import os
import argparse
from data import image_query as img_query
def main(execute_option, gg_authenticate):
    if execute_option == 1:
        imageQueries = img_query.RandomLowLightImage(gg_authenticate)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='parameters to execute main file')
    parser.add_argument('--authenticate', required=False, help='Authenticate to Google Earth Engine API', type=int, default=1)
    parser.add_argument('--execute', required=True, help='select the execute option: 1. test 1 low-light image', type=int)
    args = parser.parse_args()
    main(execute_option=args.execute, gg_authenticate=args.authenticate , sync_glc=args.sync)
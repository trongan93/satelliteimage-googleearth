
def main(execute_option, tmp):
    if execute_option == 1:
        print("Choice = 1; Sync data file from GLC to landslide short file")
    elif execute_option == 2:
        print("Choice = 2")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='parameters to execute main file')
    parser.add_argument('--execute', required=True, help='select the execute option', type=int)
    parser.add_argument('--tmp', required=False, help='tmp option')
    args = parser.parse_args()
    main(execute_option=args.execute, tmp=args.tmp)

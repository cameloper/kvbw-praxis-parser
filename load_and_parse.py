import kvbw_html_parser as kvbw
import sys
import glob

def parse_dir(dir):
    paths = glob.glob("{}/*.html".format(dir))
    print("Found {} html files in {}.".format(len(paths), dir))
    return parse(paths)

def parse(paths):
    arzts = list()
    for path in paths:
        try:
            with open(path, 'r') as f:
                p_arzts = kvbw.parse_all_resultrows(f)
                arzts = arzts + p_arzts
        except Exception as err:
            sys.exit("Could not parse file: {}.\n{}".format(path, err))

    print("Parsed total number of {} arzts.".format(len(arzts)))
    return arzts

def main():
    if len(sys.argv) < 2:
        sys.exit('Please enter a command! Valid commands are: parse-files and parse-directory.')

    command = sys.argv[1]
    if command == 'parse-files':
        if len(sys.argv) < 3:
            sys.exit('Command parse-files requires at least one file path.')
        return parse(sys.argv[2:])
    elif command == 'parse-directory':
        if len(sys.argv) != 3:
            sys.exit('Command parse-directory requires exactly one directory path.')
        return parse_dir(sys.argv[2])

if __name__ == "__main__":
    main()

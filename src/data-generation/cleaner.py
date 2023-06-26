import re
import argparse
import os


def process_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Perform the sed-like substitution and filter out lines that only contain whitespace
    non_empty_lines = [re.sub(r'^(?!Context).+', ' ', line) for line in lines if line.strip()]

    with open(input_file, 'w') as file:
        file.writelines(non_empty_lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='file', nargs='+', help='input file(s)')

    args = parser.parse_args()

    # Process each input file
    for input_file in args.files:
        if not os.path.isfile(input_file):
            print(f'Error: "{input_file}" is not a valid file.')
            continue

        process_file(input_file)


if __name__ == "__main__":
    main()

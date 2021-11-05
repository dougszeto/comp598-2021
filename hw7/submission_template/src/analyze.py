import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--coded_file')
    parser.add_argument('-o', '--output_file')

    args = parser.parse_args()
    coded_file = args.coded_file
    output_file = args.output_file

    output = {
        "course-related": 0,
        "food-related": 0,
        "residence-related": 0,
        "other": 0
    }
    convert = {
        'c': "course-related",
        'f': "food-related",
        'r': "residence-related",
        'o': "other"
    }
    with open(coded_file, 'r') as fp:
        first_line = True
        for line in fp:
            if first_line: 
                first_line = False
                continue
            split = line.split('\t')
            coding = split[2]
            if '\n' in coding:
                coding = split[2][:-1]
            output[convert[coding]]+=1
    if output_file:
        with open(output_file, 'w') as fp:
            json.dump(output, fp, indent=2)
    else:
        print(output)

if __name__ == '__main__':
    main()
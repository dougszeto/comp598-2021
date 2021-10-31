import argparse, json, datetime, pytz
'''
given a line (str of json) clean the line then return the new dictionary
'''
def clean(line):
    try:
        # try/except to catch 5
        dict = json.loads(line)
        
    except:
        return
    # 1
    if "title" not in dict and "title_text" not in dict:
        return
    # 2
    if "title_text" in dict:
        dict["title"] = dict.pop("title_text")

    # 3 and 4 check createdAt time
    if "createdAt" in dict:
        try:
            dt = datetime.datetime.strptime(dict['createdAt'], '%Y-%m-%dT%H:%M:%S%z')
            utc_time = dt.astimezone(pytz.utc)

            str_utc = utc_time.strftime('%Y-%m-%dT%H:%M:%S%z')
            dict['createdAt'] = str_utc
        except:
            return

    # 6
    if "author" not in dict or dict["author"] == None or dict["author"] == "N/A" or dict["author"] == "":
        return

    # 7
    if 'total_count' in dict:
        # 8 remove if not of type str, float, or int
        if isinstance(dict['total_count'], str) == False and isinstance(dict['total_count'], int) == False and isinstance(dict['total_count'], float) == False:
            return
        try:
            dict['total_count'] = int(float(dict['total_count']))
        except:
            return
    
    # 9 
    if 'tags' in dict:
        new_tags = []
        for tag in dict['tags']:
            words = tag.split()
            for word in words:
                new_tags.append(word)
        dict['tags'] = new_tags
    
    return dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()
    input = args.input
    output = args.output

    file = open(input, 'r')
    outfile = open(output, 'w')
    for line in file:
        cleaned = clean(line)
        if cleaned == None:
            continue
        
        # 10
        string_dict = json.dumps(cleaned)
        outfile.write(f'{string_dict}\n')
    file.close()
    outfile.close()

if __name__ == '__main__':
    main()
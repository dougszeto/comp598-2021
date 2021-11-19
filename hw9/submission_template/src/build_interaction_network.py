import pandas as pd
import json
import argparse
from pathlib import Path
import os.path as osp

def most_freq_chars(df):
    # remove the 'others', 'ponies', 'and', and 'all'
    bad_words = ['others', 'ponies', 'and ', 'all ']
    
    df = df.apply(lambda x: x.astype(str).str.lower())
    for word in bad_words:
        df = df[~df.pony.str.contains(word, regex=True)]

    # remove the one named all
    df = df[df.pony != 'all']
    n = 101
    return df['pony'].value_counts()[:n].index.tolist()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    input = args.input
    output = args.output

    # make the output directories if needed
    split_path = osp.split(output)
    output_path = split_path[0]
    Path(output_path).mkdir(parents=True, exist_ok=True)

    script_df = pd.read_csv(input)
    script_df = script_df.drop(['writer'], axis=1)

    freq_chars = most_freq_chars(script_df)

    output_dict = {}
    # group the script by episode
    grouped_df = script_df.groupby('title')
    for title in grouped_df.groups.keys():
        episode = grouped_df.get_group(title)
        # iterate through all lines in the episode
        for i in range(episode.shape[0]-1):
            cur_char = episode.iloc[i]['pony'].lower()
            next_char = episode.iloc[i+1]['pony'].lower()
            
            # skip if the current and next are the same character
            if cur_char == next_char:
                continue

            # skip if the one of the characters is not one of the most frequent
            if cur_char not in freq_chars or next_char not in freq_chars:
                continue
            
            if cur_char not in output_dict:
                output_dict[cur_char] = {next_char: 1}
            else:
                if next_char in output_dict[cur_char]:
                    output_dict[cur_char][next_char] += 1
                else:
                    output_dict[cur_char][next_char] = 1
            
            if next_char not in output_dict:
                output_dict[next_char] = {cur_char: 1}
            else:
                if cur_char in output_dict[next_char]:
                    output_dict[next_char][cur_char] += 1
                else:
                    output_dict[next_char][cur_char] = 1
    
    with open(output, 'w') as fp:
        json.dump(output_dict, fp, indent=4)

if __name__ == '__main__':
    main()
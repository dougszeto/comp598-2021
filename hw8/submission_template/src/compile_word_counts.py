import pandas as pd
import argparse
import json
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def get_stop_words(stop_words_file):
    stop_words = []
    with open(stop_words_file, 'r') as fp:
        for line in fp:
            if line[0] == '#':
                continue
            # remove the \n
            stop_words.append(line[:-1])
    return stop_words

def get_word_counts(csv_path, stop_words):
    dialog_df = pd.read_csv(csv_path)
    dialog_df = dialog_df.drop(['title', 'writer'], axis=1)

    grouped_df = dialog_df.groupby('pony')
    ponies = ['Twilight Sparkle', 'Applejack', 'Rarity', 'Pinkie Pie', 'Rainbow Dash', 'Fluttershy']
    punctuation = ['(',')','[',']',',','-','.','?','!',':',';','#','&']

    output = {}
    for pony in ponies:
        pony_lower = pony.lower()
        output[pony_lower] = {}
        try:
            df = grouped_df.get_group(pony)
        except KeyError:
            continue

        for index, row in df.iterrows():
            dialog = row['dialog']
            # remove all punctuation
            for punc in punctuation:
                if punc in dialog:
                    dialog = dialog.replace(punc, ' ')
            # split dialog by spaces
            dialog = dialog.split()
            # get word count for words that aren't in stop_words
            for word in dialog:
                word = word.lower()
                if word not in stop_words and not any(char.isdigit() for char in word):
                    if word not in output[pony_lower]:
                        output[pony_lower][word] = 1
                    else:
                        output[pony_lower][word] += 1
    # remove words with counts less than 5
    for pony in ponies:
        pony = pony.lower()
        low_freq_words = []
        word_counts = output[pony]
        for word in word_counts:
            if word_counts[word] < 5: low_freq_words.append(word)

        for word in low_freq_words:
            del word_counts[word]
        output[pony] = word_counts
    return output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-d', '--dialog')

    args = parser.parse_args()
    output = args.output

    split_path = os.path.split(output)
    output_path = split_path[0]
    Path(output_path).mkdir(parents=True, exist_ok=True)

    input_csv = args.dialog
    stop_words = get_stop_words(os.path.join(parentdir, 'data', 'stopwords.txt'))
    word_counts = get_word_counts(input_csv, stop_words)


    with open(output, 'w') as fp:
        json.dump(word_counts, fp, indent=4)
    


if __name__ == '__main__':
    main()
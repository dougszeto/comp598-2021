import json
import argparse
import math

def get_tf(word_counts, w, pony):
    return word_counts[pony][w]

def get_idf(word_counts, w):
    num_ponies = len(word_counts.keys())
    num_use_w = 0
    for pony in word_counts:
        if w in word_counts[pony]:
            num_use_w += 1
    
    return math.log(num_ponies / num_use_w)

def get_tfidf(w, pony, word_counts):
    return get_tf(word_counts, w, pony) * get_idf(word_counts, w)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--counts')
    parser.add_argument('-n', '--num')

    args = parser.parse_args()
    num = int(args.num)
    input_counts = args.counts

    word_counts = json.load(open(input_counts,'r'))

    output = {}
    for pony in word_counts:
        scores = []
        for word in word_counts[pony]:
            tfidf = get_tfidf(word, pony, word_counts)
            scores.append((word,tfidf))
        sorted_scores = sorted(scores, reverse=True, key=lambda x: x[1])
        output[pony] = []
        for i in range(num):
            output[pony].append(sorted_scores[i][0])
    print(json.dumps(output, indent=4))

if __name__ == '__main__':
    main()
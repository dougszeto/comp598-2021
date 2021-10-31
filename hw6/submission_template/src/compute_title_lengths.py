import os, sys
import argparse
import json

def main():
    input_file = sys.argv[1]

    sum_title_lengths = 0
    num_posts = 0
    with open(input_file, 'r') as fr:
        for line in fr:
            reddit_post = json.loads(line)
            post_title = reddit_post['data']['title']
            sum_title_lengths += len(post_title)
            num_posts += 1
    
    avg_title_length = sum_title_lengths / num_posts
    print(f'The average title length for posts in {input_file} is {avg_title_length} characters')

if __name__ == '__main__':
    main()
import os, sys
import random
import json

def main():
    out_file = sys.argv[2]
    json_file = sys.argv[3]
    num_posts_to_output = int(sys.argv[4])

    posts = []
    with open(json_file, 'r') as fp:
        for line in fp:
            post = json.loads(line)
            posts.append(post)

    output_posts = []
    if num_posts_to_output < len(posts):
        output_posts = random.sample(posts, num_posts_to_output)
    else:
        output_posts = posts
    
    with open(out_file, 'w') as fp:
        fp.write(f'name\ttitle\tcoding\n')
        for post in output_posts:
            name = post['data']['name']
            title = post['data']['title']
            coding = ''
            fp.write(f'{name}\t{title}\t{coding}\n')


if __name__ == '__main__':
    main()
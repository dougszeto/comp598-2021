import argparse, json, requests
def collect_newest_posts(subreddit_title):
    # set the url to the api of input subreddit
    base_url = f'https://www.reddit.com/r/{subreddit_title}/new.json'

    # change the user-agent to mimic a browser and set limit to 100 (default is 25)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}
    params = {'limit':'100'}
    # get the page
    r = requests.get(base_url, headers=header, params=params)

    # parse
    root_element = r.json()
    posts = root_element['data']['children']

    newest_posts = posts[0:100]
    for index, post in enumerate(newest_posts):
        newest_posts[index] = json.dumps(post)
    print(f'\tretrieved {len(newest_posts)} posts from {subreddit_title}')
    return newest_posts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-s', '--subreddit')

    args = parser.parse_args()
    output = args.output
    subreddit = args.subreddit

    posts = collect_newest_posts(subreddit)
    with open(output, 'w') as fp:
        for post in posts:
            fp.write(f'{post}\n')

if __name__ == '__main__':
    main()
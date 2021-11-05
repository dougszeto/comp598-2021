import os, sys
import requests
from pathlib import Path
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

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
    # define the two samples that we will look at
    sample1 = [
        'funny',
        'AskReddit',
        'gaming',
        'aww',
        'pics',
        'Music',
        'science',
        'worldnews',
        'videos',
        'todayilearned'
    ]

    sample2 = [
        'AskReddit',
        'memes',
        'politics',
        'nfl',
        'nba',
        'wallstreetbets',
        'teenagers',
        'PublicFreakout',
        'leagueoflegends',
        'unpopularopinion'
    ]
    samples = [sample1, sample2]

    # for each sample go through each subreddit and collect the 100 newest posts
    for index, sample in enumerate(samples):
        output_path = os.path.join(parentdir, f'sample{index+1}.json')
        f = open(output_path, 'w')
        print(f'Collecting posts for sample{index+1}')
        for subreddit in sample:
            posts = collect_newest_posts(subreddit)
            for post in posts:
                f.write(f'{post}\n')
        f.close()

if __name__ == '__main__':
    main()
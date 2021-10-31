import os, sys
import argparse
from pathlib import Path
import json
import os.path as osp
import requests
import bs4
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

def read_config(file_name):
    f = open(file_name, 'r')
    config = json.load(f)
    f.close()
    return config


def fetch_target_pages(target_people, cache_dir):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}
    for target in target_people:
        cache_file = osp.join(cache_dir, f'{target}.cache.html')

        if not osp.exists(cache_file):
            url = f'https://www.whosdatedwho.com/dating/{target}'
            r = requests.get(url, headers=header)
            with open(cache_file, 'w') as fw:
                fw.write(r.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_file')
    parser.add_argument('-o', '--output_file')

    args = parser.parse_args()
    config_file = args.config_file
    output_file = args.output_file

    config = read_config(config_file)
    cache_dir = config['cache_dir']
    targets = config['target_people']

    if not osp.exists(cache_dir):
        os.mkdir(cache_dir)
    
    fetch_target_pages(targets, cache_dir)

    output_dict = {}
    
    for target in targets:
        # keep track of the targets partners
        partners = []
        cache_file = osp.join(cache_dir, f'{target}.cache.html')

        # find the h4 with the correct class name!
        soup = bs4.BeautifulSoup(open(cache_file, 'r'), 'html.parser')
        relationships_header = soup.find('h4', 'ff-auto-relationships')
        current_element = relationships_header.find_next_sibling()

        # go through every p sibling of the h4
        while current_element.name == 'p':
            # get the links in this p tag
            links = current_element.find_all('a')
            for link in links:
                href = link['href']
                temp = href.split('/')
                partners.append(temp[2])
            current_element = current_element.find_next_sibling() 
        
        output_dict[target] = partners
        
    with open(output_file, 'w') as fp:
        json.dump(output_dict, fp, indent=4)
        
        

if __name__ == '__main__':
    main()
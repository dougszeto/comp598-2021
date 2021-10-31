import pandas as pd
import sys, json

output_path = sys.argv[2]
data_path = sys.argv[3]

df = pd.read_csv(data_path)
count = {
    "twilight sparkle": 0,
    "applejack": 0,
    "rarity": 0,
    "pinkie pie": 0,
    "rainbow dash": 0,
    "fluttershy": 0
}

for pony in count.keys():
    temp = df['pony'].str.fullmatch(pony, case=False)
    num = len(temp[temp==True].index)
    count[pony] = num

verbosity = {
    "twilight sparkle": 0,
    "applejack": 0,
    "rarity": 0,
    "pinkie pie": 0,
    "rainbow dash": 0,
    "fluttershy": 0
}

for pony in verbosity.keys():
    num_lines = count[pony]
    total_lines = df.shape[0]
    verbosity[pony] = round(num_lines / total_lines, 2)

dictionary = {
    "count": count,
    "verbosity": verbosity
}

with open(output_path, 'w') as out:
    json.dump(dictionary, out, indent=4)
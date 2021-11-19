import networkx as nx
from networkx.algorithms.shortest_paths import weighted
import pandas as pd
import json
import argparse
from pathlib import Path
import os.path as osp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    input = args.input
    output = args.output

    interaction_network = None
    with open(input, 'r') as fp:
        interaction_network = json.load(fp)
    
    # make the graph
    graph = nx.Graph()
    for speaker in interaction_network:
        for listener in interaction_network[speaker]:
            if graph.has_edge(speaker, listener): continue
            graph.add_edge(speaker, listener, weight=interaction_network[speaker][listener])

    # get most connected by num
    degrees = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    output_dict = {}
    most_connected_by_num = [degrees[0][0], degrees[1][0], degrees[2][0]]
    output_dict['most_connected_by_num'] = most_connected_by_num

    # get most connected by weight
    weighted_degrees = sorted(graph.degree(weight='weight'), key=lambda x: x[1], reverse=True)
    most_connected_by_weight = [weighted_degrees[0][0], weighted_degrees[1][0], weighted_degrees[2][0]]
    output_dict['most_connected_by_weight'] = most_connected_by_weight

    # get most central by betweeness
    betweeness = sorted(nx.betweenness_centrality(graph).items(), key=lambda x: x[1], reverse=True)
    most_central = [betweeness[0][0], betweeness[1][0], betweeness[2][0]]
    output_dict['most_central_by_betweenness'] = most_central

    # write to output file
    split_path = osp.split(output)
    output_path = split_path[0]
    Path(output_path).mkdir(parents=True, exist_ok=True)
    with open(output, 'w') as fp:
        json.dump(output_dict, fp, indent=4)

    
if __name__ == '__main__':
    main()
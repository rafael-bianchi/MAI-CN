import statistics

import networkx as nx
import requests
import numpy as np
from lxml import etree
from sklearn.preprocessing import MinMaxScaler


def get_content(url):
    response = requests.get(url)
    if (not response.ok and (response.reason == 'Not Found' or response.reason == 'Bad Request')):
        print (f'Error: {response.text}')
        return []

    data = response.content
    tree = etree.fromstring(data)

    return tree


def rescale_weights(graph, min=0, max=1,percentile=90):
    edges_weights = {(u,v): [d['weight']] for (u, v, d) in graph.edges(data=True)}

    scaler = MinMaxScaler(feature_range=(min,max))
    weights = scaler.fit_transform(list(edges_weights.values()))

    scaler = MinMaxScaler(feature_range=(0.01,1))
    colors = scaler.fit_transform(list(edges_weights.values()))
    edges_colors = {}

    idx = 0
    for key in edges_weights.keys():
        graph.edges[(key[0], key[1])]['weight'] = weights[idx][0]
        edges_weights[(key[0], key[1])] = weights[idx][0]
        edges_colors[(key[0], key[1])] = colors[idx]
        
        idx += 1

    return edges_weights, edges_colors, statistics.median(weights[0]), np.percentile(weights, 90)

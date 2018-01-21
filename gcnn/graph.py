import numpy as np
import scipy as sp
import scipy.sparse, scipy.linalg
import networkx as nx


def grid_coordinates(n: int):
    """
    Coordinates (x, y) list for a grid of size n x n.
    """
    idx = np.arange(n)
    return np.reshape(np.meshgrid(idx, idx), (2, -1)).T


def knn(z, k: int = 4, metric: str = 'euclidean'):
    """
    K-NN adjacency matrix from list of features. Might return more than k neighbors in case of distance equality.
    """
    dists = sp.spatial.distance.pdist(z, metric)
    dists = sp.spatial.distance.squareform(dists)
    
    weights = np.exp(- dists ** 2 / 2)
    mask = weights < np.sort(weights, axis=1)[:, -k]
    weights[mask & mask.T] = 0
    
    assert np.all(weights == weights.T)
    return weights


def kwraps(n: int, k: int = 1):
    """
    Adjacency matrix from a wrapped grid (border touch other borders) within k elements. Not optimized.
    """
    
    adj = np.zeros([n ** 2, n ** 2])

    def add_edge(x1, y1, x2, y2, v=1):
        i = np.ravel_multi_index((x1, y1), (n, n))
        j = np.ravel_multi_index((x2, y2), (n, n))   
        adj[i, j] = v

    for x in range(n):
        for y in range(n):
            for dx in range(-k, k + 1):
                for dy in range(-k, k + 1):
                    if dx != 0 or dy != 0:
                        add_edge(x, y, (x + dx) % n, (y + dy) % n)  
    
    return adj


def kwraps3d(n: int, k: int = 1, d: int = 2):
    """
    NetworkX graph from a wrapped 3d grid (border touch other borders) within k elements. Not optimized.
    """
    
    g = nx.empty_graph()

    def add_edge(x1, y1, z1, x2, y2, z2, v=1):
        g.add_edge((x1, y1, z1), (x2, y2, z2))   

    for x in range(n):
        for y in range(n):
            for z in range(d):
                for dx in range(-k, k + 1):
                    for dy in range(-k, k + 1):
                        for dz in range(-k, k + 1):
                            if dx != 0 or dy != 0 or dz != 0:
                                add_edge(x, y, z, (x + dx) % n, (y + dy) % n, (z + dz) % d)  
    
    return g


def fourier(laplacian):
    """
    Graph fourier basis for a laplacian using SVD.
    """
    return sp.linalg.svd(laplacian)[0]


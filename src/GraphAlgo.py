import random
from typing import List

from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph, NodeData
import math
import queue
import matplotlib.pyplot as plt
import numpy as np


class GraphAlgo(GraphAlgoInterface):
    """
    This class represents algorithms on directed weighted graphs.
    This class includes methods:
    to save and load graph from JSON files.
    to compute shortest path from a node to another and return it and it's weight.
    to compute connected components of either node or entire graph and return it.
    """

    def __init__(self, graph: DiGraph):
        self.graph = graph

    def get_graph(self) -> DiGraph:
        """
        :return: the directed weighted graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        pass

    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """
        node_src = self.graph.vertex.get(id1)
        node_dest = self.graph.vertex.get(id2)
        self.set_graph_to_inf()
        node_src.weight = 0
        q = queue.PriorityQueue()
        parents = {}
        path = []
        q.put(node_src)
        while not q.empty():
            node_curr = q.get()
            if node_curr.tag < 0:
                node_curr.tag = 1
                for key in self.graph.all_out_edges_of_node(node_curr.key).keys():
                    node = self.graph.vertex.get(key)
                    dist = node_curr.weight + node_curr.edges_out.get(key)
                    if dist < node.weight:
                        node.weight = dist
                        parents[node] = node_curr
                    q.put(node)
        if node_dest.weight == math.inf:
            return math.inf, []
        else:
            node = node_dest
            while node is not None:
                path.append(node)
                node = parents.get(node)
            path.reverse()
        return node_dest.weight, path

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        x_list = []
        y_list = []
        key_list = []
        for node in self.graph.get_all_v().values():
            if node.pos is None:
                node.pos = (random.randrange(25), random.randrange(25), random.randrange(25))
            x_list.append(node.pos[0])
            y_list.append(node.pos[1])
            key_list.append(node.key)
        fig, ax = plt.subplots()
        ax.scatter(x_list, y_list)
        for i, txt in enumerate(key_list):
            ax.annotate(key_list[i], {x_list[i], y_list[i]})
        plt.title("graph")
        plt.plot(x_list, y_list, ".", color='red')
        for node in self.graph.get_all_v().values():
            x_src = node.pos[0]
            y_src = node.pos[1]
            for edge in self.graph.all_out_edges_of_node(node.key).keys():
                node_dest = self.graph.vertex.get(edge)
                x_dest = node_dest.pos[0]
                y_dest = node_dest.pos[1]
                plt.arrow(x_src, y_src, (x_dest - x_src), (y_dest - y_src), length_includes_head=True, width=0.0001,
                          head_width=0.3, color='black')
        plt.show()

    def set_graph_to_inf(self):
        """method to help with dijkstra algorithm, initializing all nodes weight to infinite"""
        for node in self.graph.get_all_v().values():
            node.weight = math.inf
            node.tag = -1

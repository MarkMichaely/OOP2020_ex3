import json
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

    def __init__(self, graph: DiGraph = DiGraph()):
        self.graph = graph

    def get_graph(self) -> DiGraph:
        """
        :return: the directed weighted graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "r") as o:
                json_string = json.load(o)
            g = DiGraph()
            for node in json_string["Nodes"]:
                if "pos" in node:
                    pos = tuple(map(float, str(node["pos"]).split(",")))
                    g.add_node(node_id=node["id"], pos=pos)
                else:
                    g.add_node(node_id=node["id"])

            for edge in json_string["Edges"]:
                g.add_edge(id1=edge["src"], id2=edge["dest"], weight=edge["w"])
            self.graph = g
            return True
        except IOError as e:
            print(e)

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "w") as o:
                json.dump(self.graph.to_json(), default=lambda a: a.to_json(), fp=o)
        except IOError as e:
            print(e)

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
        if id1 not in self.graph.get_all_v().keys() or id2 not in self.graph.get_all_v().keys():
            return math.inf, []
        node_src = self.graph.vertex.get(id1)
        node_dest = self.graph.vertex.get(id2)
        self.set_graph_to_inf()
        node_src.weight = 0
        q = queue.PriorityQueue()
        parents = {}
        path = []
        q.put(node_src)
        visited = set()
        while not q.empty():
            node_curr = q.get()
            if node_curr not in visited:
                visited.add(node_curr)
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
                path.append(node.key)
                node = parents.get(node)
            path.reverse()
        return node_dest.weight, path

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC

        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        if self.graph is None or id1 not in self.graph.get_all_v():
            return []
        self.set_graph_to_inf()
        scc = self.__kosaraju(id1)
        return scc

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        Notes:
        If the graph is None the function should return an empty list []
        """
        if self.graph is None:
            return [[]]
        self.set_graph_to_inf()
        scc_list = []
        for node in self.graph.get_all_v().keys():
            if self.graph.vertex.get(node).tag == 0:
                scc = self.__kosaraju(node)
                for n in scc:
                    self.graph.vertex.get(n).tag = 1
                scc_list.append(scc)
        return scc_list

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        x_list = []
        y_list = []
        key_list = []
        for node in self.graph.get_all_v().values():
            if node.pos is None:
                node.pos = (np.random.randint(0, 30), np.random.randint(0, 30), np.random.randint(0, 30))
            x_list.append(node.pos[0])
            y_list.append(node.pos[1])
            key_list.append(node.key)
        fig, ax = plt.subplots()
        ax.scatter(x_list, y_list)
        for i, txt in enumerate(key_list):
            ax.annotate(key_list[i], {x_list[i], y_list[i]})
        plt.plot(x_list, y_list, ".", color='red')
        for node in self.graph.get_all_v().values():
            x_src = node.pos[0]
            y_src = node.pos[1]
            for edge in self.graph.all_out_edges_of_node(node.key).keys():
                node_dest = self.graph.vertex.get(edge)
                x_dest = node_dest.pos[0]
                y_dest = node_dest.pos[1]
                plt.arrow(x_src, y_src, (x_dest - x_src), (y_dest - y_src), length_includes_head=True, width=0.00001,
                          head_width=0.00006, color='black')
        plt.title("graph")
        plt.show()

    def set_graph_to_inf(self):
        """method to help with dijkstra algorithm, initializing all nodes weight to infinite"""
        for node in self.graph.get_all_v().values():
            node.weight = math.inf
            node.tag = 0

    def __kosaraju(self, src: int):
        visited_in = set()
        visited_out = set()
        stack_out = [src]
        stack_in = [src]
        while stack_out:
            pop = stack_out.pop()
            if pop not in visited_in:
                visited_in.add(pop)
                for node in self.graph.all_out_edges_of_node(pop).keys():
                    stack_out.append(node)
        while stack_in:
            pop = stack_in.pop()
            if pop not in visited_out:
                visited_out.add(pop)
                for node in self.graph.all_in_edges_of_node(pop).keys():
                    stack_in.append(node)
        common = visited_in - (visited_in - visited_out)
        return list(common)

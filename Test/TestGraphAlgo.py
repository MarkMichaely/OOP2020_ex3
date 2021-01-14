import json
import unittest
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
import numpy as np


class TestGraphAlgo(unittest.TestCase):
    def create_graph_10(self):
        g = DiGraph()
        for key in range(10):
            g.add_node(key)
        return g

    def create_graph_small(self):
        g = DiGraph()
        g.add_node(1)
        g.add_node(3)
        g.add_node(2)
        g.add_edge(1, 2, 1)
        g.add_edge(1, 3, 1)
        g.add_edge(2, 3, 1)
        g.add_edge(3, 2, 1)
        return g

    def test_get_graph(self):
        g = self.create_graph_10()
        g_algo = GraphAlgo(g)
        self.assertIsNotNone(g_algo)
        self.assertIsNotNone(g_algo.get_graph())
        self.assertTrue(0 in g_algo.get_graph().vertex)
        self.assertFalse(10 in g_algo.get_graph().vertex)

    def test_load_from_json(self):
        g_algo = GraphAlgo()
        file = '../data/T0.json'
        g_algo.load_from_json(file)
        self.assertTrue(g_algo.get_graph().v_size(), 4)
        self.assertTrue(0 in g_algo.get_graph().vertex)
        self.assertFalse(4 in g_algo.get_graph().vertex)
        self.assertTrue(1 in g_algo.get_graph().all_in_edges_of_node(0))

    def test_save_to_json(self):
        g = self.create_graph_small()
        g_algo = GraphAlgo(g)
        file = "../data/TestJson1.json"
        g_algo.save_to_json(file)
        try:
            with open(file, "r") as o:
                json_string = json.load(o)
        except IOError as e:
            print(e)
        self.assertIsNotNone(json_string)

    def test_shortest_path(self):
        g = self.create_graph_small()
        g_algo = GraphAlgo(g)
        dist, path = g_algo.shortest_path(3, 1)
        self.assertEqual(dist, np.inf)
        self.assertEqual(path, [])
        dist, path = g_algo.shortest_path(3, 2)
        self.assertEqual(dist, 1)
        self.assertEqual(path, [3, 2])

    def test_connected_component(self):
        g = self.create_graph_small()
        g_algo = GraphAlgo(g)
        l = g_algo.connected_component(1)
        self.assertEqual(l, [1])
        self.assertEqual(g_algo.connected_component(2), g_algo.connected_component(3))
        g_algo.get_graph().add_node(0)
        g_algo.get_graph().add_edge(0, 1, 1)
        g_algo.get_graph().add_edge(1, 0, 1)
        self.assertEqual(g_algo.connected_component(1), g_algo.connected_component(0))
        g_algo.get_graph().add_edge(2, 0, 1)
        self.assertEqual(g_algo.connected_component(0), [0, 1, 2, 3])

    def test_connected_components(self):
        g = self.create_graph_small()
        g_algo = GraphAlgo(g)
        self.assertEqual(g_algo.connected_components(), [[1], [2, 3]])
        g_algo.get_graph().add_node(0)
        g_algo.get_graph().add_edge(0, 1, 1)
        g_algo.get_graph().add_edge(1, 0, 1)
        self.assertEqual(g_algo.connected_components(), [[0, 1], [2, 3]])
        g_algo.get_graph().add_edge(2, 0, 1)
        self.assertEqual(g_algo.connected_components(), [[0, 1, 2, 3]])

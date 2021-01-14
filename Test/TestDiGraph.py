import unittest
from src.DiGraph import DiGraph


class TestDiGraph(unittest.TestCase):
    def create_graph_10(self):
        g = DiGraph()
        for key in range(10):
            g.add_node(key)
        return g

    def create_graph_20(self):
        g = DiGraph()
        for key in range(20):
            g.add_node(key)
        return g

    def test_graph_creation(self):
        g = DiGraph()
        self.assertIsNotNone(g)

    def test_vertex_size(self):
        g = DiGraph()
        self.assertEqual(g.v_size(), 0)
        g = self.create_graph_10()
        self.assertEqual(g.v_size(), 10)
        g = self.create_graph_20()
        self.assertNotEqual(g.v_size(), 10)
        self.assertEqual(g.v_size(), 20)

    def test_edge_size(self):
        g = DiGraph()
        self.assertEqual(g.e_size(), 0)
        g.add_node(0)
        g.add_node(1)
        g.add_edge(1, 0, 1)
        self.assertEqual(g.e_size(), 1)
        g.add_edge(0, 1, 2)
        self.assertEqual(g.e_size(), 2)
        g.add_edge(0, 1, 4)
        self.assertEqual(g.e_size(), 2)

    def test_get_all_v(self):
        g = self.create_graph_10()
        v10_list = g.get_all_v()
        g = self.create_graph_20()
        v20_list = g.get_all_v()
        self.assertNotEqual(v20_list, v10_list)
        self.assertTrue(0 in v10_list.keys())
        self.assertTrue(0 in v20_list.keys())
        self.assertTrue(9 in v10_list.keys())
        self.assertTrue(9 in v20_list.keys())
        self.assertTrue(10 in v20_list.keys())
        self.assertFalse(10 in v10_list.keys())

    def test_all_in_edges_of_node(self):
        g = self.create_graph_10()
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(0, 3, 1)
        g.add_edge(0, 4, 1)
        g.add_edge(2, 1, 1)
        g.add_edge(3, 1, 1)
        g.add_edge(4, 1, 1)
        self.assertEqual(g.all_in_edges_of_node(0), {})
        e_list = g.all_in_edges_of_node(1)
        self.assertTrue(0 in e_list.keys())
        self.assertFalse(5 in e_list.keys())
        self.assertTrue(2 in e_list.keys())
        self.assertEqual(len(g.all_in_edges_of_node(1)), 4)
        self.assertEqual(len(g.all_in_edges_of_node(2)), 1)
        self.assertEqual(len(g.all_in_edges_of_node(3)), 1)
        self.assertEqual(len(g.all_in_edges_of_node(0)), 0)

    def test_all_out_edges_of_node(self):
        g = self.create_graph_10()
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        g.add_edge(0, 3, 1)
        g.add_edge(0, 4, 1)
        g.add_edge(2, 1, 1)
        g.add_edge(3, 1, 1)
        g.add_edge(4, 1, 1)
        self.assertEqual(len(g.all_out_edges_of_node(0)), 4)
        self.assertEqual(len(g.all_out_edges_of_node(1)), 0)
        self.assertEqual(len(g.all_out_edges_of_node(4)), 1)
        self.assertTrue(1 in g.all_out_edges_of_node(0).keys())
        self.assertTrue(1 in g.all_out_edges_of_node(2).keys())
        self.assertFalse(1 in g.all_out_edges_of_node(5).keys())
        self.assertFalse(5 in g.all_out_edges_of_node(0).keys())

    def test_get_mc(self):
        g = DiGraph()
        self.assertEqual(g.get_mc(), 0)
        g.add_node(1)
        g.add_node(2)
        self.assertEqual(g.get_mc(), 2)
        g.add_edge(1, 2, 1)
        self.assertEqual(g.get_mc(), 3)
        g.add_edge(1, 2, 333)
        self.assertEqual(g.get_mc(), 3)
        g.remove_edge(1, 2)
        g.add_edge(1, 2, 1)
        self.assertEqual(g.get_mc(), 5)
        g.add_edge(2, 1, 1)
        g.remove_node(1)
        self.assertEqual(g.get_mc(), 7)

    def test_add_edge(self):
        g = DiGraph()
        self.assertEqual(g.e_size(), 0)
        g.add_node(1)
        g.add_node(2)
        flag = g.add_edge(1, 2, 999)
        self.assertTrue(flag)
        self.assertEqual(g.e_size(), 1)
        self.assertTrue(2 in g.all_out_edges_of_node(1))
        self.assertTrue(1 in g.all_in_edges_of_node(2))
        self.assertFalse(2 in g.all_in_edges_of_node(1))
        self.assertFalse(1 in g.all_out_edges_of_node(2))
        flag = g.add_edge(2, 1, 111)
        self.assertTrue(flag)
        flag = g.add_edge(2, 1, 222)
        self.assertFalse(flag)
        self.assertEqual(g.e_size(), 2)
        self.assertTrue(2 in g.all_in_edges_of_node(1))
        self.assertTrue(1 in g.all_out_edges_of_node(2))
        self.assertNotEqual(g.all_in_edges_of_node(1)[2], g.all_in_edges_of_node(2)[1])
        self.assertEqual(g.all_in_edges_of_node(1)[2], g.all_out_edges_of_node(2)[1])
        self.assertEqual(g.all_in_edges_of_node(1)[2], 111)

    def test_add_node(self):
        g = DiGraph()
        self.assertEqual(g.v_size(), 0)
        flag = g.add_node(1)
        self.assertEqual(g.v_size(), 1)
        self.assertTrue(flag)
        g.add_node(2)
        self.assertEqual(g.v_size(), 2)
        self.assertTrue(1 in g.vertex)
        self.assertTrue(2 in g.vertex)
        flag = g.add_node(2)
        self.assertEqual(g.v_size(), 2)
        self.assertFalse(flag)

    def test_remove_node(self):
        g = DiGraph()
        self.assertEqual(g.v_size(), 0)
        g.add_node(1)
        self.assertEqual(g.v_size(), 1)
        flag = g.remove_node(1)
        self.assertEqual(g.v_size(), 0)
        self.assertTrue(flag)
        flag = g.remove_node(1)
        self.assertFalse(flag)

    def test_remove_edge(self):
        g = DiGraph()
        self.assertEqual(g.e_size(), 0)
        g.add_node(1)
        g.add_node(2)
        flag = g.add_edge(1, 2, 999)
        self.assertTrue(flag)
        self.assertEqual(g.e_size(), 1)
